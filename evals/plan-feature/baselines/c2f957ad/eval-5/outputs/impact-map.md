# TC-9005 — Repository Impact Map and Plan

Feature: **TC-9005 — Drop status table and migrate to enum column**
Priority: **High** | Fix Versions: **RHTPA 2.0.0**

## Run context and non-interactive decisions

| Step | Prompt / decision | Choice made (non-interactive default) |
|---|---|---|
| 0 | Project Configuration validation | Passed: Repository Registry, Jira Configuration (Project key TC, Cloud ID, Feature type 10142) and Code Intelligence present in CLAUDE.md |
| 0.5 | Jira access method | Offline eval — no MCP/REST calls; all Jira writes captured as files in this directory |
| 1 | Feature fetch | Read from `evals/plan-feature/files/feature-feature-branch.md`. Priority = `High` (set, not "Undefined"); fixVersions = `[RHTPA 2.0.0]` (non-empty) |
| 1 | Documentation signals | "Documentation Considerations" present -> doc impact type **Updates to existing content** (Minor: internal architecture docs). Documentation task generated (Task 6) |
| 1.5 | Link Feature to a parent issue? | Skipped (Enter) — Feature has no parent; none provided |
| 2 | Figma | No Figma URL in arguments or description — step skipped (backend-only feature) |
| 2.5 | Issue type discovery | Could not query Jira offline; no level-1 (Epic) type could be confirmed -> graceful degradation: **Feature -> Task** hierarchy, no Epics created. (CLAUDE.md `Default epic grouping strategy: by-sub-feature` is recorded but not applied because no Epic type was discovered) |
| 3 | Target repository | `trustify-backend` (from `repo-backend.md`; no Serena instance -> analysis from the provided structure with Read) |
| 4 | Impact map approval | Auto-approved |
| 4.5 | Workflow mode | **feature-branch** (see below) |
| 5 | Bookend idempotency guard | Feature `Linked Issues: None` -> no existing "Create/Merge feature branch" tasks -> bookends generated |
| 6a | `workflow:feature-branch` label on the Feature | **Will be applied** (appended to existing label `ai-generated-jira`) |

## Repository Impact Map

```
trustify-backend:
  changes:
    - Add an atomic, reversible migration that creates enum type advisory_status_enum (New, Analyzing, Fixed, Rejected), adds and backfills advisory.status, drops advisory.status_id and its FK, and drops the advisory_status table
    - Register the new migration in the migrator
    - Update the SeaORM advisory entity to expose an AdvisoryStatus enum column and remove the status_id field, the advisory_status relation, and the advisory_status entity
    - Update AdvisoryService fetch/list/search queries to use advisory.status with no advisory_status join
    - Update AdvisorySummary / AdvisoryDetails models to read status from advisory.status (response shape unchanged)
    - Update the advisory list endpoint status filter and get endpoint to use the enum column
    - Update SearchService advisory search to use advisory.status with no join
    - Update the advisory ingestion pipeline to write the enum status directly (no lookup-table insert), failing closed on unknown statuses
    - Update advisory/search integration tests for the enum-backed status
    - Update internal architecture docs to reflect the schema change
```

### Files analyzed (from repository structure)

| Area | Paths |
|---|---|
| Migration | `migration/src/lib.rs`, `migration/src/m0001_initial/mod.rs` (defines current `advisory_status` / `status_id`), new `migration/src/m0002_advisory_status_enum/mod.rs` |
| Entity | `entity/src/advisory.rs`, `entity/src/lib.rs`, `entity/src/sbom_advisory.rs` (reference) |
| Advisory read path | `modules/fundamental/src/advisory/service/advisory.rs`, `model/summary.rs`, `model/details.rs`, `endpoints/list.rs`, `endpoints/get.rs` |
| Search | `modules/search/src/service/mod.rs` |
| Ingestion | `modules/ingestor/src/graph/advisory/mod.rs`, `modules/ingestor/src/service/mod.rs`, `modules/ingestor/src/graph/sbom/mod.rs` (reference) |
| Shared utilities (reuse) | `common/src/db/query.rs`, `common/src/model/paginated.rs`, `common/src/error.rs` |
| Tests | `tests/api/advisory.rs`, `tests/api/search.rs` |
| Docs | `README.md`, `CONVENTIONS.md` (no `docs/testing-readiness.md` -> no testing tasks generated) |

### Conventions

`CONVENTIONS.md` exists at the repository root; its contents were taken from the "Key Conventions" section of the repository description (Framework, Module pattern, Error handling, Endpoint registration, Response types, Query helpers, Testing, Caching). Each convention was checked for file-type/scope applicability per `shared/convention-applicability-rules.md`; only applicable conventions appear in task Implementation Notes, each with an `Applies:` rationale (applied in Task 4).

### Open questions / discrepancies (recorded, not blocking)

1. **`entity/advisory_status.rs` not found.** The feature requires removing `entity/advisory_status.rs`, but the analyzed `entity/src/` directory does not contain that file. Task 3 instructs the implementer to delete it if present, or remove the inline lookup-entity definition from `entity/src/advisory.rs` otherwise.
2. **"Remove the `advisory_status` table and its migration history."** Planned as a forward-only drop in a new migration (`m0002_advisory_status_enum`). The already-applied `m0001_initial` migration is not rewritten, since that would break databases that have already run it. Confirm with the feature owner if a migration squash is actually wanted.
3. **Additional call sites.** The structure shows only the advisory module and the search module as lookup-table consumers. Task 4 requires a repository-wide grep for `advisory_status|status_id` and an update of any further call sites (e.g., SBOM details that embed advisories).

### Excluded requirements

None. All 7 MVP requirements map to tasks:

| Requirement | Task |
|---|---|
| Create enum type `advisory_status_enum` (reversible) | Task 2 |
| Add `status` column, backfill from `status_id` join | Task 2 |
| Drop `status_id` FK column | Task 2 |
| Drop `advisory_status` table | Task 2 |
| Update all advisory queries (service + endpoints) | Task 4 |
| Update SeaORM entities (`advisory.rs`, remove `advisory_status`) | Task 3 |
| Update ingestion to write enum directly | Task 5 |
| NFR: migration atomic | Task 2 (fail-closed AC + rollback test) |
| NFR: zero downtime / production-sized dataset test | Task 2 (Implementation Notes; PR note) |
| NFR: all changes land together | feature-branch mode + bookend Tasks 1 and 7 |
| Documentation Considerations | Task 6 |

## Workflow Mode Decision (Step 4.5)

**Selected mode: `feature-branch`**

Atomicity indicators found:

1. **Coordinated schema migrations (present).** Task 2 drops `advisory.status_id` and the `advisory_status` table. Tasks 3, 4, and 5 depend on the new `advisory.status` column and the removal of the lookup entity. Merging Task 2 alone breaks every advisory query and the ingestion path, which still join or write `advisory_status`. Merging Tasks 3–5 alone references a `status` column that does not exist yet.
2. **Cross-cutting refactors (present).** Removing the `advisory_status` entity and adding `AdvisoryStatus` (Task 3) is a shared-type change used by the advisory service, endpoints, and search (Task 4) and by ingestion (Task 5). Partial delivery leaves the workspace failing to compile.
3. Breaking API changes: not present. The public response shape is unchanged.
4. Tightly coupled frontend/backend: not present (backend only).

The feature's NFR states this directly: "All changes must land together."

Interdependent tasks: Task 2 (migration) <-> Task 3 (entity) <-> Task 4 (queries) and Task 5 (ingestion). Task 6 (docs) describes the combined result.

Consequences:
- Bookend Task 1 (`create-branch`, Target Branch `main`) and Task 7 (`merge-branch`, Target Branch `main`) are generated.
- All intermediate Tasks 2–6 use Target Branch **`TC-9005`**.
- Every non-documentation intermediate task (2, 3, 4, 5) lists Task 1 as a direct dependency.
- Task 7 depends on all intermediate tasks (2, 3, 4, 5, 6).
- The `workflow:feature-branch` label will be applied to feature TC-9005 in Step 6a.

## Task Plan

| # | Summary | Target Branch | Bookend Type | Dependencies | File |
|---|---|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | main | create-branch | — | `task-1-create-feature-branch.md` |
| 2 | Add atomic migration replacing advisory_status table with advisory_status_enum column | TC-9005 | — | 1 | `task-2-advisory-status-enum-migration.md` |
| 3 | Update SeaORM advisory entity to use AdvisoryStatus enum | TC-9005 | — | 1, 2 | `task-3-update-seaorm-advisory-entity.md` |
| 4 | Update advisory queries to use status enum column instead of join | TC-9005 | — | 1, 3 | `task-4-advisory-queries-use-status-column.md` |
| 5 | Update advisory ingestion to write status enum directly | TC-9005 | — | 1, 3 | `task-5-ingestion-write-status-enum.md` |
| 6 | Update internal architecture docs for advisory status enum | TC-9005 | — | 2, 3, 4, 5 | `task-6-update-architecture-docs.md` |
| 7 | Merge feature branch TC-9005 to main | main | merge-branch | 2, 3, 4, 5, 6 | `task-7-merge-feature-branch.md` |

## Inherited Field Values (`additional_fields` for every created task)

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

- **priority**: Feature priority is `High` (set, not "Undefined"). It is **propagated** to all 7 tasks.
- **fixVersions**: Feature has `[RHTPA 2.0.0]` and CLAUDE.md `fixVersion scope: both`. It is **propagated** to all 7 tasks.
- **labels**: `ai-generated-jira` is set on every task.
- No Epics are created (no level-1 type discovered), so no Epic `additional_fields` apply.

Per-task creation details, digests, and links are in `task-creation-log.md`.
