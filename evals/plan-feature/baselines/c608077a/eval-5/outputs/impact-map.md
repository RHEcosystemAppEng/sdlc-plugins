# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

(This content would be posted as a Jira comment on TC-9005 via `jira.add_comment` after user approval. Approval assumed for this eval run.)

```
trustify-backend:
  changes:
    - Add an atomic, reversible migration that creates the advisory_status_enum type (New, Analyzing, Fixed, Rejected), adds and backfills advisory.status from the status_id join, drops advisory.status_id and its FK, and drops the advisory_status table
    - Register the new migration in the migration crate
    - Update the SeaORM advisory entity to expose a typed AdvisoryStatus enum column and remove the status_id field / advisory_status relation
    - Remove the advisory_status SeaORM entity
    - Update AdvisoryService fetch/list/search queries and advisory models to read advisory.status with no join
    - Update the advisory list endpoint status filter to filter on advisory.status
    - Update SearchService advisory search to stop referencing advisory_status
    - Update the advisory ingestion pipeline to write enum values directly (no lookup-table insert) and reject unknown statuses
    - Update advisory and search integration tests
    - Update internal architecture documentation for the schema change
```

## Affected paths (from repository analysis of repo-backend.md)

| Area | Path | Change |
|---|---|---|
| Migration | `migration/src/lib.rs` | modify — register `m0002_advisory_status_enum` |
| Migration | `migration/src/m0002_advisory_status_enum/mod.rs` | create |
| Migration | `migration/src/m0001_initial/mod.rs` | reference only — must NOT be edited |
| Entity | `entity/src/advisory.rs` | modify — `status: AdvisoryStatus` |
| Entity | `entity/src/lib.rs` | modify — remove `advisory_status` module |
| Service | `modules/fundamental/src/advisory/service/advisory.rs` | modify — drop join |
| Model | `modules/fundamental/src/advisory/model/summary.rs`, `details.rs` | modify |
| Endpoint | `modules/fundamental/src/advisory/endpoints/list.rs` | modify — status filter |
| Search | `modules/search/src/service/mod.rs` | modify — drop lookup reference |
| Ingestion | `modules/ingestor/src/graph/advisory/mod.rs` | modify — write enum directly |
| Ingestion | `modules/ingestor/src/service/mod.rs` | modify (conditional) — error propagation |
| Tests | `tests/api/advisory.rs`, `tests/api/search.rs` | modify |

## Producer / consumer trace for the advisory status data

- **Writers (producers):** migration backfill (Task 2, one-time) and advisory ingestion pipeline `modules/ingestor/src/graph/advisory/mod.rs` (Task 5, insert + re-ingest/update paths). No other writer of advisory status is visible in the repository structure.
- **Readers (consumers):** `AdvisoryService` + advisory models + list/get endpoints (Task 4), `SearchService` (Task 4). Potential additional reader: `modules/fundamental/src/sbom/service/sbom.rs` if SBOM details embed advisory status via `entity/src/sbom_advisory.rs` — Task 4 requires a grep for `advisory_status|status_id` and inclusion of any extra hits.

## Analysis notes and assumptions

- **Target repository:** the CLAUDE.md Repository Registry lists only `sdlc-plugins`; the target repository for this feature is `trustify-backend` as given by the eval fixture `repo-backend.md`. No Serena instance is configured — analysis was done from the provided repository structure manifest.
- **`entity/src/advisory_status.rs`:** named by the Feature for removal but not present in the repository manifest. Task 3 instructs the implementer to verify its location and delete it (or the inline definition) accordingly; it is not listed under Files to Modify because the path could not be confirmed.
- **CONVENTIONS.md:** present at the repository root; its content was taken from the "Key Conventions" section of the manifest (Framework, Module pattern, Error handling, Endpoint registration, Response types, Query helpers, Testing, Caching). Conventions were applied per task only where the task's files match the convention scope.
- **Migration history:** the goal "remove the `advisory_status` table and its migration history" is planned as a forward drop migration; `m0001_initial` is left immutable to avoid breaking already-migrated databases.
- **Testing readiness template:** `docs/testing-readiness.md` is not present in the repository manifest — no cross-cutting testing tasks generated.
- **Figma:** no Figma link in the Feature — Step 2 skipped.
- **Parent link (Step 1.5):** Feature has no parent; prompt skipped (assumed user pressed Enter).

## Excluded requirements

None. All seven MVP requirements are covered:

| Requirement | Task(s) |
|---|---|
| Create `advisory_status_enum` (reversible) | Task 2 |
| Add + backfill `advisory.status` | Task 2 |
| Drop `status_id` FK column | Task 2 |
| Drop `advisory_status` table | Task 2 |
| Update all advisory queries | Task 4 |
| Update SeaORM entities | Task 3 |
| Update ingestion pipeline | Task 5 |
| Documentation Considerations (Minor, internal architecture docs) | Task 6 |

NFR coverage: atomic migration (Task 2 single transaction + rollback test), zero downtime (Task 2 notes: short transaction, coordinated deploy, production-sized dataset test), all changes land together (feature-branch workflow).

## Workflow mode

**feature-branch** — see `workflow-mode-comment.md`. The `workflow:feature-branch` label will be added to TC-9005 (preserving existing label `ai-generated-jira`) after all tasks are created.

## Issue types and hierarchy (Step 2.5)

Jira could not be queried in this eval; assumed the TC project exposes the standard Jira Cloud hierarchy:
- Feature: Feature (ID 10142, level 2) — from CLAUDE.md
- Epic: Epic (level 1) — assumed present
- Task: Task (level 0)

Epic grouping strategy: `by-sub-feature` (from CLAUDE.md `## Hierarchy Configuration`). Suggested groupings (approval assumed):

| Epic | Summary | Tasks |
|---|---|---|
| Epic A | TC-9005: Advisory status schema and entity migration | Task 2, Task 3 |
| Epic B | TC-9005: Advisory query and ingestion updates | Task 4, Task 5 |
| Epic C | TC-9005: Feature branch lifecycle and documentation | Task 1, Task 6, Task 7 |

## Inherited field values (`additional_fields`)

- Feature priority: **High** (set, not "Undefined") → propagated to every Epic and Task.
- Feature fixVersions: **RHTPA 2.0.0** (non-empty); CLAUDE.md `fixVersion scope: both` → propagated to every Epic and Task.

`additional_fields` applied to every created Epic and Task:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

Full per-issue log: `task-creation-log.md`.

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
