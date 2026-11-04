# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## Planning context

| Step | Outcome |
|---|---|
| Step 0: Project Configuration | Valid. Repository Registry, Jira Configuration (project TC, cloud ID, feature type 10142), and Code Intelligence are present. |
| Step 1: Feature fetch | TC-9005 read from `feature-feature-branch.md` (mock). Priority: **High**. fixVersions: **[RHTPA 2.0.0]**. Labels: `ai-generated-jira`. |
| Step 1: Documentation signals | Documentation Considerations section present. Doc impact: **Updates to existing content (Minor)**, meaning internal architecture docs. Reference: SeaORM enum mapping docs. A documentation task is generated (Task 5). |
| Step 1.5: Parent link | The Feature has no parent. Eval run is non-interactive, so the parent-link prompt was skipped. |
| Step 2: Figma | No Figma URL in the arguments or the description. Skipped (backend-only feature). |
| Step 2.5: Issue types | Jira is not reachable in this eval, and no level-1 (Epic) type was supplied. **No Epic-level type found in project. Tasks will be created directly under the Feature.** The `Hierarchy Configuration` default (`by-sub-feature`) is therefore not applied. |
| Step 3: Repository analysis | No Serena instance is configured. Analysis used the repository manifest `repo-backend.md`. CONVENTIONS.md is present at the repo root, and its conventions are taken from the manifest's Key Conventions section (Framework, Module pattern, Error handling, Endpoint registration, Response types, Query helpers, Testing, Caching). No `docs/testing-readiness.md` exists, so no testing tasks are generated. |

## Shared-artifact producer and consumer analysis — `advisory.status` (formerly `advisory.status_id` -> `advisory_status`)

| Role | Path | Covered by |
|---|---|---|
| Producer: one-time backfill | `migration/src/m0002_advisory_status_enum/mod.rs` (new), registered in `migration/src/lib.rs` | Task 2 |
| Producer: runtime ingestion writer | `modules/ingestor/src/graph/advisory/mod.rs` | Task 4 |
| Producer: ingestion orchestration and error propagation | `modules/ingestor/src/service/mod.rs` | Task 4 |
| Schema definition | `entity/src/advisory.rs`, `entity/src/lib.rs`, `entity/src/advisory_status.rs` (delete; not in manifest, so verify it exists) | Task 3 |
| Consumer: advisory service (fetch, list, search) | `modules/fundamental/src/advisory/service/advisory.rs` | Task 3 |
| Consumer: advisory list endpoint (status filter, UC-1) | `modules/fundamental/src/advisory/endpoints/list.rs` | Task 3 |
| Consumer: advisory get endpoint | `modules/fundamental/src/advisory/endpoints/get.rs` | Task 3 |
| Consumer: response models | `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/advisory/model/details.rs` | Task 3 |
| Consumer: cross-entity search | `modules/search/src/service/mod.rs` | Task 3 |
| Consumer: SBOM-advisory queries (via `sbom_advisory`) | `modules/fundamental/src/sbom/service/sbom.rs` (audit) | Task 3 |
| Tests | `tests/api/advisory.rs`, `tests/api/search.rs`, migration tests | Tasks 2, 3, 4 |

Without code intelligence, Task 3 requires a `grep -rn "advisory_status\|status_id\|StatusId"` sweep before implementation. The grep result is authoritative, and any additional call site it finds is in scope.

## Impact map

```
trustify-backend:
  changes:
    - Add a single atomic, reversible migration that creates advisory_status_enum (New, Analyzing, Fixed, Rejected), adds and backfills advisory.status, makes it NOT NULL, drops advisory.status_id, and drops the advisory_status table, failing closed on unmappable rows
    - Update SeaORM entities: add the AdvisoryStatus active enum and status field on advisory, remove status_id, and remove the advisory_status entity and its relations
    - Remove the advisory_status join from the advisory service, the list (status filter) and get endpoints, the response models, the search service, and the SBOM-advisory queries, with the API response shape unchanged
    - Update advisory ingestion to map feed status strings to AdvisoryStatus and write the enum directly, failing closed on unknown statuses
    - Update internal architecture documentation for the new advisory status schema
```

## Excluded requirements / open questions

- **"Remove the `advisory_status` table and its migration history"** (Goal statement): the table drop is planned in Task 2. Rewriting or deleting migration history (`migration/src/m0001_initial/mod.rs`) is **excluded**, because applied migrations are immutable and editing them would break existing databases. Missing input: confirmation from the feature owner that "migration history" means the forward drop and not a history rewrite.
- **Zero downtime vs. dropping columns in the same migration** (NFR): dropping `status_id` and `advisory_status` while pre-TC-9005 instances are still serving will break those instances. A strict zero-downtime rollout would need an expand/contract split across releases, which conflicts with the "migration must be atomic" and "all changes land together" NFRs. The plan follows the explicit atomicity NFR and documents a coordinated migration-plus-binary rollout (Tasks 2 and 6). Missing input: the deployment strategy decision from DevOps.
- **"Reduce advisory list endpoint p95 latency by ~40ms"** (Goal): there is no benchmark harness in the repository (no `docs/testing-readiness.md`, no perf tests in the manifest), so this cannot be decomposed into a verifiable task. It is noted for post-merge measurement.
- **`entity/src/advisory_status.rs`** is named in the Feature but absent from the repository manifest. Task 3 instructs the implementer to verify its location before deleting it.

## Workflow mode decision (Step 4.5)

**Selected mode: `feature-branch`**

Atomicity indicators found:
1. **Coordinated schema migration.** Task 2 drops `advisory.status_id` and `advisory_status`, while Tasks 3 and 4 contain the code that stops referencing them. Merging Task 2 alone breaks every advisory query. Merging Task 3 or 4 alone references an `advisory.status` column that does not exist.
2. **Cross-cutting refactor.** Removing `advisory_status::Entity` and `advisory::Column::StatusId` (Task 3) breaks compilation of the ingestor until Task 4 lands, so partial delivery leaves `main` non-compiling.

The Feature's own NFR also states: "All changes must land together."

Interdependent tasks: Task 2 (migration) <-> Task 3 (entities and query layer) <-> Task 4 (ingestion).

The `workflow:feature-branch` label will be applied to the feature issue TC-9005 in Step 6a, appended to the existing labels: `["ai-generated-jira", "workflow:feature-branch"]`.

## Task plan

| # | Task | Target Branch | Depends on |
|---|---|---|---|
| 1 | Create feature branch TC-9005 from main (bookend: create-branch) | main | — |
| 2 | Add advisory_status_enum migration | TC-9005 | 1 |
| 3 | Update SeaORM entities and advisory query layer to use the status enum column | TC-9005 | 1, 2 |
| 4 | Write advisory status enum directly in the ingestion pipeline | TC-9005 | 1, 2, 3 |
| 5 | Update internal architecture docs for advisory status enum (documentation) | TC-9005 | 2, 3, 4 |
| 6 | Merge feature branch TC-9005 to main (bookend: merge-branch) | main | 2, 3, 4, 5 |

Bookend idempotency guard: TC-9005 has no linked issues ("Linked Issues: None"), so no existing "Create/Merge feature branch" tasks were found and the bookends are generated.

Epic grouping: not applied, because no level-1 issue type is available.

## Inherited field propagation (`additional_fields` for every created task)

| Field | Feature value | Rule | Propagated value |
|---|---|---|---|
| labels | — | Always | `["ai-generated-jira"]` |
| priority | High | Set (not "Undefined"), so inherit | `{"name": "High"}` |
| fixVersions | [RHTPA 2.0.0] | Non-empty, and `fixVersion scope: both` in CLAUDE.md Jira Field Defaults, so inherit | `[{"name": "RHTPA 2.0.0"}]` |

```json
"additional_fields": {
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

See `task-creation-log.md` for per-task creation parameters, links, and digests.

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
