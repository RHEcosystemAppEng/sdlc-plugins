# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

> This file is the content of the impact map comment that would be posted on TC-9005 (Step 4), with the workflow mode decision appended (Step 4.5).

## Planning context

- **Feature:** TC-9005, priority High, fixVersions RHTPA 2.0.0, labels `ai-generated-jira`
- **Figma:** none linked, so the Figma step was skipped (backend-only feature)
- **Parent link (Step 1.5):** no parent set and none supplied, so the step was skipped
- **Code intelligence:** no Serena instance is configured for `trustify-backend`. Analysis used the repository structure fixture (`repo-backend.md`).
- **CONVENTIONS.md:** present at the repository root. The conventions applied in tasks are Query helpers, Error handling, Response types, and Testing.
- **Testing readiness template (`docs/testing-readiness.md`):** not found, so no testing tasks were generated
- **Documentation signals:** "Documentation Considerations" was found with doc impact "Minor — update internal architecture docs" (classified as **Updates**), so one documentation task was generated
- **Issue types (Step 2.5):** Jira was not reachable in this eval run, so issue types could not be discovered. The plan uses graceful degradation (Feature → Task, no Epics, no error). If a level-1 type is discovered in a live run, CLAUDE.md `Default epic grouping strategy: by-sub-feature` applies. Proposed groups: "TC-9005: Feature branch lifecycle" (Tasks 1 and 6), "TC-9005: Schema & data access migration" (Tasks 2–4), and "TC-9005: Documentation" (Task 5). These groups need user approval.

## Impact map

```
trustify-backend:
  changes:
    - Add a reversible, atomic migration that creates the advisory_status_enum type (New, Analyzing, Fixed, Rejected), adds advisory.status, and backfills it from the status_id join
    - Fail the migration closed (full rollback) when any advisory row has no resolvable status after the backfill
    - Drop the advisory.status_id FK column after the backfill, then drop the advisory_status lookup table
    - Register the new migration in the migration crate
    - Model advisory_status_enum as a SeaORM ActiveEnum on the advisory entity, replace status_id with status, and remove the advisory_status entity
    - Change AdvisoryService fetch, list, and search and the advisory list/get endpoints to read and filter advisory.status directly (no join), keeping the response shape unchanged
    - Update every other consumer of the advisory_status entity (search service, SBOM service advisory loading, shared query helpers, if referenced)
    - Change the advisory ingestion pipeline to map feed status strings to the enum and write them directly, rejecting unknown statuses
    - Update integration tests and fixtures that seed advisory_status
    - Update internal architecture docs for the new schema
```

## Shared-artifact producer and consumer analysis (`advisory.status`)

| Role | Path | Coverage |
|---|---|---|
| Producer (one-time backfill) | `migration/src/m0002_advisory_status_enum/mod.rs` (new), registered in `migration/src/lib.rs` | Task 2: backfill, fail-closed, round-trip tests |
| Producer (runtime: ingestion) | `modules/ingestor/src/graph/advisory/mod.rs` | Task 4: per-status, update, and fail-closed tests |
| Producer (runtime: ingestion service entry) | `modules/ingestor/src/service/mod.rs` | Task 4 |
| Schema definition | `entity/src/advisory.rs`, `entity/src/lib.rs` | Task 3 |
| Consumer | `modules/fundamental/src/advisory/service/advisory.rs` (fetch/list/search) | Task 3 |
| Consumer | `modules/fundamental/src/advisory/model/summary.rs`, `details.rs` | Task 3 |
| Consumer | `modules/fundamental/src/advisory/endpoints/list.rs`, `get.rs` | Task 3: filter and shape tests in `tests/api/advisory.rs` |
| Possible consumer (to verify) | `modules/search/src/service/mod.rs` | Task 3: conditional, found by cross-cutting grep. Tests in `tests/api/search.rs` |
| Possible consumer (to verify) | `modules/fundamental/src/sbom/service/sbom.rs` (advisories via `entity/src/sbom_advisory.rs`) | Task 3: conditional. Tests in `tests/api/sbom.rs` |
| Possible consumer (to verify) | `common/src/db/query.rs` | Task 3: conditional |

No fallback, recovery, or on-demand write paths for advisory status appear in the repository structure. There is no manual or API write endpoint for advisories, only `GET` routes. Because no Serena instance exists, the implementer must confirm this with the workspace-wide grep defined in Tasks 3 and 4.

## Unverified paths

- `entity/advisory_status.rs` (named in the Feature requirements): **not present** in the repository structure available during planning (`entity/src/` lists `advisory.rs`, `sbom.rs`, `sbom_advisory.rs`, `package.rs`, `sbom_package.rs`, `package_license.rs`). Task 3 tells the implementer to find the lookup entity definition and remove it, without listing an unconfirmed path under Files to Modify.

## Risks and open questions

1. **Zero-downtime and atomic drop conflict (needs product owner input).** The NFRs require a single atomic migration that drops `status_id` and `advisory_status`, and they also require zero downtime while the application serves traffic. Pre-TC-9005 application instances that are still running will fail on advisory queries the moment the migration commits, because they join the dropped table. Rewriting `advisory` during the backfill also takes table locks. The two requirements can only both hold if migration and deployment are coordinated (for example, migrate as part of a rolling deploy with a brief read-only window), or if the work is split into expand and contract releases. An expand/contract split would contradict "all changes must land together" and "drop in the same migration". The plan follows the explicit requirements (one atomic migration). Please confirm the deployment strategy before Task 6 merges.
2. **Silent data loss risk in the backfill.** Orphaned or unmappable `status_id` values would leave `status` NULL, and dropping the lookup table would then destroy the source data. Task 2 lowers this risk into a fail-closed acceptance criterion with a matching test (the migration errors and rolls back).
3. **Silent default risk in ingestion.** With the lookup table removed, unknown feed statuses can no longer be added as new rows. Task 4 requires an error, not a silent default to `New`.
4. **Production-sized dataset test:** listed in Customer Considerations. It is a pre-merge check in Task 6 (operational, in addition to the code-level coverage above).

## Excluded requirements

None. All seven MVP requirements map to tasks:

| Requirement | Task |
|---|---|
| Create enum type `advisory_status_enum` (reversible) | Task 2 |
| Add `status` column, backfilled in the same migration | Task 2 |
| Drop `status_id` FK column | Task 2 |
| Drop `advisory_status` lookup table | Task 2 |
| Update all advisory queries (service and endpoints) | Task 3 |
| Update SeaORM entity definitions | Task 3 |
| Update ingestion pipeline to write enum values directly | Task 4 |
| Documentation (Minor, internal architecture docs) | Task 5 |

The goal "Reduce advisory list endpoint p95 latency by ~40ms" is an expected outcome, not a task. No benchmark harness exists in the repository and no `docs/testing-readiness.md` performance category was found, so no performance testing task was generated.

---

## Workflow mode decision (Step 4.5)

**Selected mode: `feature-branch`**

**Atomicity indicators found:**
1. **Coordinated schema migration.** Task 2 drops `advisory.status_id` and `advisory_status`. Task 3 (entity and queries) and Task 4 (ingestion) depend on the new `advisory.status` column and on the lookup table being gone. Merging Task 2 alone to `main` breaks every advisory query. Merging Task 3 or 4 alone references a column that does not exist. The Feature's NFR states this directly: "All changes must land together".
2. **Cross-cutting refactor.** Removing the `advisory_status` SeaORM entity and `advisory::Column::StatusId` changes a shared type used by the fundamental advisory module, the ingestor, and possibly the search and SBOM modules. Partial delivery leaves the workspace failing to compile.

No breaking API change: the response shape is unchanged. No frontend/backend coupling: the feature is backend only.

**Interdependent tasks:** Task 2 ↔ Task 3 ↔ Task 4 (migration, entity and readers, writer). Task 5 documents the combined result.

**Branch plan:** Task 1 creates `TC-9005` from `main`. Tasks 2–5 target `TC-9005`. Task 6 merges `TC-9005` into `main`. The `workflow:feature-branch` label will be applied to TC-9005 in Step 6a. Its existing label `ai-generated-jira` is preserved.

**Bookend idempotency guard:** TC-9005 has no linked issues (`Linked Issues: None`), so no existing "Create feature branch" or "Merge feature branch" tasks were found and bookend tasks were generated.

---

## Field values for created issues (`additional_fields`)

The source is TC-9005: priority `High`, fixVersions `[RHTPA 2.0.0]`. CLAUDE.md Jira Field Defaults sets `fixVersion scope: both`, so fixVersions are propagated to tasks.

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

These fields apply to all six tasks. Issue type: Task (level 0, resolved dynamically in a live run). Parent: none (no Epic type discovered in this run). See `task-creation-log.md`.

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
