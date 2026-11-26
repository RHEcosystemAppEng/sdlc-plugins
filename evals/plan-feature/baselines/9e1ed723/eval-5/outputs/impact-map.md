# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## Planning Context (Steps 0 – 2.5)

| Item | Value |
|---|---|
| Project Configuration (Step 0) | Valid — Repository Registry, Jira Configuration (key `TC`, Cloud ID, Feature type ID `10142`), Code Intelligence present |
| Feature | TC-9005 — "Drop status table and migrate to enum column" |
| Feature priority (Step 1) | `High` → **propagated** to all created issues |
| Feature fixVersions (Step 1) | `RHTPA 2.0.0` → **propagated** to all created tasks (`fixVersion scope: both`) |
| Feature labels | `ai-generated-jira` (preserved; `workflow:feature-branch` appended in Step 6a) |
| Parent link (Step 1.5) | Feature has no parent; interactive prompt skipped in eval (no parent key supplied) — no link created |
| Documentation signals (Step 1) | Present — Doc impact type: **Updates to existing content** ("Minor — update internal architecture docs to reflect schema change"); no external API doc changes; reference: SeaORM enum mapping docs |
| Figma (Step 2) | No Figma URL in arguments or description — skipped (backend-only feature) |
| Issue types (Step 2.5) | Live discovery not possible in eval (no Jira access). Treated as **no level-1 (Epic) type discovered** → graceful degradation to Feature → Task hierarchy; "Incorporates" links go Feature → Task. (Hierarchy Configuration `by-sub-feature` would apply only if an Epic-level type is discovered at run time.) |
| Code intelligence (Step 3) | No Serena instance for `trustify-backend`; analysis based on the repository structure fixture (`repo-backend.md`) |
| CONVENTIONS.md (Step 3) | Present at repo root. Conventions used: Framework (Axum/SeaORM), Module pattern, Error handling, Endpoint registration, Response types, Query helpers, Testing, Caching |
| Docs discovered (Step 3) | `README.md`, `CONVENTIONS.md` (no `docs/` directory, no OpenAPI spec, no architecture doc) |
| Testing readiness template (Step 3) | `docs/testing-readiness.md` **not present** in `trustify-backend` → no testing tasks generated |
| Eval infrastructure (Step 3) | Not applicable — no task modifies a skill `SKILL.md` |
| Bookend idempotency guard | Feature has no linked issues → no existing "Create/Merge feature branch" tasks → bookends generated |

## Impact Map

```
trustify-backend:
  changes:
    - Add a reversible, transactional migration that creates PostgreSQL enum type advisory_status_enum (New, Analyzing, Fixed, Rejected), adds advisory.status, backfills it from the advisory_status join, drops advisory.status_id and drops the advisory_status table
    - Register the new migration in the migrator
    - Update the SeaORM Advisory entity to expose a `status` enum column (DeriveActiveEnum) instead of the `status_id` FK/relation, and remove the advisory_status entity
    - Update AdvisoryService queries (fetch, list, search) to read/filter on advisory.status without joining advisory_status
    - Update AdvisorySummary / AdvisoryDetails mapping so the API still returns status as the same string (no response-shape change)
    - Update the advisory list endpoint status filter to filter on the enum column
    - Update SearchService advisory queries that read advisory status (remove advisory_status join)
    - Update the advisory ingestion pipeline to map feed status strings to advisory_status_enum and write advisory.status directly (no lookup-table insert)
    - Update advisory integration tests for status filtering, response shape and ingestion
    - Update internal architecture documentation (README.md data-model notes) for the new schema
```

## Shared-Artifact Producer / Consumer Analysis (Step 3)

Shared artifact: **advisory status** (`advisory.status_id` + `advisory_status` table today → `advisory.status` enum column after the change).

| Role | Path | Workflow | Covered by |
|---|---|---|---|
| Producer (one-time backfill) | `migration/src/m0002_advisory_status_enum/mod.rs` (new) | Migration backfill from existing join | Task 2 |
| Producer (primary writer) | `modules/ingestor/src/graph/advisory/mod.rs` | Advisory feed ingestion (parse, store, correlate) | Task 5 |
| Producer (orchestration) | `modules/ingestor/src/service/mod.rs` | `IngestorService` — entry point that dispatches advisory ingestion (verify for any lookup-table seeding / status upsert) | Task 5 |
| Schema definition | `entity/src/advisory.rs`, `entity/src/lib.rs` | SeaORM model used by all readers/writers | Task 3 |
| Consumer | `modules/fundamental/src/advisory/service/advisory.rs` | `AdvisoryService` fetch, list, search | Task 4 |
| Consumer | `modules/fundamental/src/advisory/model/summary.rs`, `details.rs` | API response mapping | Task 4 |
| Consumer | `modules/fundamental/src/advisory/endpoints/list.rs` | `GET /api/v2/advisory` status filter | Task 4 |
| Consumer | `modules/fundamental/src/advisory/endpoints/get.rs` | `GET /api/v2/advisory/{id}` | Task 4 |
| Consumer | `modules/search/src/service/mod.rs` | `SearchService` full-text search across entities (includes advisories) | Task 4 |
| Tests | `tests/api/advisory.rs`, `tests/api/search.rs` | Endpoint + ingestion integration tests | Tasks 4, 5 |

No fallback/recovery, scheduled, or manual/API status-update writer was found in the repository structure (there is no advisory status update endpoint). The implementer of Task 5 must confirm with a repo-wide search for `advisory_status` / `status_id` that no other writer exists; any additional writer found must be added to that task before merge.

## Unresolved Items / Clarifications Needed

1. **`entity/src/advisory_status.rs` not found in the repository structure.** The Feature requirement says "remove `entity/advisory_status.rs`", but the entity directory listing contains only `sbom.rs`, `advisory.rs`, `sbom_advisory.rs`, `package.rs`, `sbom_package.rs`, `package_license.rs`. The lookup table may be modelled inline in `entity/src/advisory.rs` or the file may be missing from the fixture. Task 3 instructs the implementer to delete the file if it exists and remove the inline definition otherwise; it is not listed in Files to Modify because the path could not be confirmed.
2. **"Remove the `advisory_status` table and its migration history".** Rewriting `migration/src/m0001_initial/mod.rs` would break databases that have already applied it. The plan drops the table in a **new forward migration** (with a `down()` that recreates it) and leaves `m0001_initial` untouched. Please confirm this interpretation; if you really want the initial migration edited, that needs a separate decision.
3. **Zero-downtime vs atomic single release.** The NFRs require both an atomic migration and zero downtime. Because the old code joins `advisory_status`, running the migration while old binaries serve traffic will break their queries for the length of the rollout. The plan meets "atomic" (single transaction) and "all changes land together" (feature-branch mode). True zero downtime would need an expand/contract rollout across releases, which goes against "all changes must land together". Flagged for stakeholder decision; it does not block the tasks.
4. **Production-sized dataset testing** (Customer Considerations) is an operational pre-deployment activity. It is recorded here and in Task 2's Test Requirements as a migration performance check, but no repository artifact supports it.

## Excluded Requirements

None. All seven MVP requirements are covered by Tasks 2–5. The documentation consideration is covered by Task 6.

## Workflow Mode Decision (Step 4.5)

**Mode: `feature-branch`**

Atomicity indicators found:
- **Coordinated schema migration**: Task 2 (migration drops `status_id` and `advisory_status`) and Tasks 3/4/5 (entity, queries, ingestion) depend on the same schema change. Merging the migration alone breaks every advisory query, and merging the code alone references a column that does not exist. The Feature NFR says so directly: "All changes must land together".
- **Cross-cutting refactor**: the `Advisory` entity's `status_id` → `status` change touches every reader and writer (fundamental advisory module, search module, ingestor). Delivering only part of it leaves `main` in an inconsistent, non-compiling state.

Interdependent tasks: Task 2 ↔ Task 3 ↔ Task 4 ↔ Task 5. All target branch `TC-9005`. Intermediate builds on `TC-9005` may fail between Task 3 and Tasks 4/5. That is expected, and `main` is protected until Task 7 merges.

The `workflow:feature-branch` label will be applied to TC-9005 in Step 6a. Existing label `ai-generated-jira` is preserved.

## Task Plan

| # | Summary | Target Branch | Depends on |
|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | main | — |
| 2 | Add reversible migration replacing advisory_status table with advisory_status_enum column | TC-9005 | 1 |
| 3 | Update SeaORM Advisory entity to use status enum column | TC-9005 | 1, 2 |
| 4 | Remove advisory_status join from advisory and search queries | TC-9005 | 1, 3 |
| 5 | Write advisory status enum directly in ingestion pipeline | TC-9005 | 1, 3 |
| 6 | Update internal architecture docs for advisory status enum | TC-9005 | 1, 2, 3, 4, 5 |
| 7 | Merge feature branch TC-9005 to main | main | 1, 2, 3, 4, 5, 6 |

## Task Creation Log (Step 6 — simulated)

Hierarchy: Feature → Task (no Epic-level type discovered; Step 6a.0 skipped).

`additional_fields` applied to **every** created task (Tasks 1–7):

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

- `priority`: Feature priority `High` (not "Undefined") → included.
- `fixVersions`: Feature has `RHTPA 2.0.0` and `fixVersion scope: both` → included.
- `parent`: omitted (no Epics).
- Issue type: Task (level-0 type from Step 2.5 discovery).

| # | Placeholder key | Summary | Digest comment file |
|---|---|---|---|
| 1 | TC-9005-T1 | Create feature branch TC-9005 from main | task-1-digest.md |
| 2 | TC-9005-T2 | Add reversible migration replacing advisory_status table with advisory_status_enum column | task-2-digest.md |
| 3 | TC-9005-T3 | Update SeaORM Advisory entity to use status enum column | task-3-digest.md |
| 4 | TC-9005-T4 | Remove advisory_status join from advisory and search queries | task-4-digest.md |
| 5 | TC-9005-T5 | Write advisory status enum directly in ingestion pipeline | task-5-digest.md |
| 6 | TC-9005-T6 | Update internal architecture docs for advisory status enum | task-6-digest.md |
| 7 | TC-9005-T7 | Merge feature branch TC-9005 to main | task-7-digest.md |

Feature label update (after all tasks created):

```
jira.edit_issue("TC-9005", fields={"labels": ["ai-generated-jira", "workflow:feature-branch"]})
```

### Issue links (Step 6b)

Incorporates (inward TC-9005 → outward task): T1, T2, T3, T4, T5, T6, T7.

Depend (inward = dependent, outward = dependency):

| Dependent | Depends on |
|---|---|
| T2 | T1 |
| T3 | T1, T2 |
| T4 | T1, T3 |
| T5 | T1, T3 |
| T6 | T1, T2, T3, T4, T5 |
| T7 | T1, T2, T3, T4, T5, T6 |
