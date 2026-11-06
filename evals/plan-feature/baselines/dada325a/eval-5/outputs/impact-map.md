# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## Context gathered

- **Feature:** TC-9005, Priority **High**, Fix Versions **RHTPA 2.0.0**, Labels `ai-generated-jira`, no linked issues, no parent set.
- **Figma:** none (backend-only feature; Step 2 skipped).
- **Parent link (Step 1.5):** no parent on the Feature. The user prompt was skipped in this non-interactive eval, so no parent was linked.
- **Code intelligence:** no Serena instance configured. The analysis used the repository structure fixture (`repo-backend.md`).
- **CONVENTIONS.md:** listed at the `trustify-backend` repository root, but its contents were not available in this eval. Task Implementation Notes cite the repository's documented Key Conventions instead (Axum/SeaORM, `model/ + service/ + endpoints/`, `Result<T, AppError>` with `.context()`, `PaginatedResults<T>`, `common/src/db/query.rs` helpers, `tests/api/` integration tests).
- **Documentation files found:** `README.md` and `CONVENTIONS.md`.
- **Documentation signals (Step 1):** "Documentation Considerations" is present, with impact type **Updates to existing content** (Minor, internal architecture docs). A documentation task is generated.
- **Testing readiness template:** `docs/testing-readiness.md` was not found in `trustify-backend`, so no testing tasks are generated.
- **Issue types (Step 2.5):** project issue-type metadata was not available in this eval, and no level-1 (Epic) type was discovered. **No Epic-level type found in project — tasks will be created directly under the Feature.** The `## Hierarchy Configuration` default (`by-sub-feature`) would apply if an Epic type existed.
  - Type-to-role mapping: Feature (ID 10142, from CLAUDE.md); Epic: none; Task: `Task`.

## Repository Impact Map

```
trustify-backend:
  changes:
    - Add a reversible, single-transaction migration that creates advisory_status_enum (New, Analyzing, Fixed, Rejected), adds and backfills advisory.status, drops advisory.status_id and its FK, and drops the advisory_status table, failing closed if any row cannot be mapped
    - Register the new migration in the migrator
    - Update the SeaORM advisory entity to use an AdvisoryStatus active enum for the status column and remove the advisory_status entity and relation
    - Remove the advisory_status join from all advisory reads (AdvisoryService fetch/list/search, list/get endpoints, summary/details models), keeping the API response shape unchanged
    - Filter advisories by status on the enum column directly; reject invalid filter values with 400
    - Update every other consumer of advisory_status/status_id (search service, shared query helpers if enum filtering needs support, integration tests)
    - Update the advisory ingestion pipeline to map feed status strings to AdvisoryStatus and write them directly, rejecting unknown statuses
    - Update internal architecture documentation for the new schema
```

## Shared-artifact producer / consumer trace

The shared artifact is the advisory status value, stored in `advisory.status` (previously `advisory.status_id` → `advisory_status`).

| Role | Path | Covered by |
|---|---|---|
| Producer (schema / backfill) | `migration/src/m0002_advisory_status_enum/mod.rs` (new), `migration/src/lib.rs` | Task 2 |
| Producer (type definition) | `entity/src/advisory.rs`, `entity/src/lib.rs` | Task 3 |
| Producer (primary write: feed ingestion) | `modules/ingestor/src/graph/advisory/mod.rs` | Task 5 |
| Producer (on-demand / service entry) | `modules/ingestor/src/service/mod.rs` (`IngestorService`) | Task 5 (verify and update if it writes status) |
| Producer (re-ingest / update path) | `modules/ingestor/src/graph/advisory/mod.rs` | Task 5 (re-ingest test) |
| Consumer | `modules/fundamental/src/advisory/service/advisory.rs` | Task 4 |
| Consumer | `modules/fundamental/src/advisory/endpoints/list.rs`, `get.rs` | Task 4 |
| Consumer | `modules/fundamental/src/advisory/model/summary.rs`, `details.rs` | Task 4 |
| Consumer | `modules/search/src/service/mod.rs` | Task 4 |
| Consumer (filter helper) | `common/src/db/query.rs` | Task 4 |
| Tests | `tests/api/advisory.rs`, `tests/api/search.rs` | Task 4 |
| Possible consumer (unconfirmed) | `modules/fundamental/src/sbom/service/sbom.rs` (if SBOM details read advisory status through `sbom_advisory`) | Task 4: a mandatory grep for `advisory_status`/`status_id` must cover it if found |

## Discrepancies and clarifications

1. **`entity/advisory_status.rs` is not in the repository structure.** The Feature asks to remove `entity/advisory_status.rs`, but `entity/src/` only lists `sbom.rs`, `advisory.rs`, `sbom_advisory.rs`, `package.rs`, `sbom_package.rs` and `package_license.rs`. Task 3 tells the implementer to check whether the lookup entity is a separate file or defined inline. It is not listed as a guaranteed path.
2. **"Remove the `advisory_status` table and its migration history" (goal) vs "Migration must be reversible" (requirement).** The plan drops the table through a new forward migration and does **not** rewrite `migration/src/m0001_initial/mod.rs`, because rewriting an applied migration breaks existing databases. Please confirm this reading. If literal removal from `m0001_initial` is wanted, it needs a separate decision.
3. **Zero-downtime NFR vs dropping `status_id` in the same migration.** Application instances on the old code still read `status_id`/`advisory_status`. With an all-or-nothing migration (required by the atomicity NFR), zero downtime holds only if the migration and the new code are deployed together. Task 2 asks for lock and duration figures from a production-sized dataset, and Task 7 carries the deployment note. If strict zero downtime with rolling deploys is required, an expand/contract split (add column, deploy code, then drop) would be needed. That conflicts with the "single atomic migration" NFR and needs stakeholder input.

## Excluded requirements

| Requirement / goal | Reason not planned as a task |
|---|---|
| "Reduce advisory list endpoint p95 latency by ~40ms" (goal) | No performance benchmark harness or testing readiness template (`docs/testing-readiness.md`) exists in the repo. Task 4 has an optional item to capture the query plan or latency before and after, but there is no verifiable benchmark task. |
| "Migration must be tested against a production-sized dataset before deployment" (Customer Considerations) | Operational activity that needs a production-sized dataset, which the repository analysis cannot provide. It is a Test Requirement in Task 2 (record timing in the PR), not a separate code task. |

All seven MVP requirements are covered:

| Requirement | Task(s) |
|---|---|
| Create enum type | Task 2 |
| Add and backfill `status` | Task 2 |
| Drop `status_id` | Task 2 |
| Drop `advisory_status` table | Task 2 |
| Update all advisory queries | Task 4 |
| Update SeaORM entities | Task 3 |
| Update ingestion | Task 5 |

## Workflow mode decision (Step 4.5)

**Mode: `feature-branch`**

Atomicity indicators found:

1. **Coordinated schema migrations:** Task 2 drops `advisory.status_id` and the `advisory_status` table and adds `advisory.status`. Tasks 3, 4 and 5 depend on that schema. Merging Task 2 alone breaks every advisory query, which still joins the dropped table. Merging Tasks 3–5 alone references a column that does not exist. The Feature's NFR says so directly: "All changes must land together".
2. **Cross-cutting refactor:** removing `advisory::Model.status_id` and the `advisory_status` entity (Task 3) changes a shared type used by the fundamental, search and ingestor modules (Tasks 4 and 5). Partial delivery would not compile.

Interdependent tasks: Task 2 ↔ Task 3 ↔ Task 4 ↔ Task 5.

- Intermediate tasks (2–6) target branch `TC-9005`.
- Bookend tasks (1 and 7) target `main`.
- The `workflow:feature-branch` label will be added to TC-9005 in Step 6a, preserving the existing `ai-generated-jira` label.

**Bookend idempotency guard:** TC-9005 has no linked issues, so there are no existing "Create feature branch" or "Merge feature branch" tasks. Bookends are generated.

## Task list

| # | Summary | Target Branch | Depends on |
|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | main | — |
| 2 | Add reversible migration converting advisory_status lookup table to advisory_status_enum column | TC-9005 | 1 |
| 3 | Update SeaORM advisory entity to use AdvisoryStatus enum column and remove advisory_status entity | TC-9005 | 1, 2 |
| 4 | Replace advisory_status joins with the advisory.status enum column in all advisory queries | TC-9005 | 1, 3 |
| 5 | Update advisory ingestion pipeline to write AdvisoryStatus enum values directly | TC-9005 | 1, 3 |
| 6 | Update internal architecture docs for advisory status enum column | TC-9005 | 2, 3, 4, 5 |
| 7 | Merge feature branch TC-9005 to main | main | 2, 3, 4, 5, 6 |

## Inherited field values (`additional_fields` for every created task)

- Feature priority: **High** (set, not "Undefined"), so it is propagated.
- Feature fixVersions: **RHTPA 2.0.0**. `fixVersion scope: both` in Jira Field Defaults, so it is propagated.

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

No Epics are created (no level-1 type), so no `parent` field is set on the tasks.

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
