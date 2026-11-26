# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## Step 0 / 1 summary

- Project Configuration validated in CLAUDE.md (Repository Registry, Jira Configuration, Code Intelligence present).
- Feature: **TC-9005** — Drop status table and migrate to enum column
- Priority: **High** (set — will be propagated)
- Fix Versions: **RHTPA 2.0.0** (set; `fixVersion scope: both` — will be propagated to Epics and Tasks)
- Figma: none (backend-only feature; Step 2 skipped)
- Parent link (Step 1.5): Feature has no parent; interactive prompt not answerable in eval mode — skipped (optional step).
- Documentation signals: **Updates to existing content** ("Doc Impact: Minor — update internal architecture docs to reflect schema change"; reference material: SeaORM enum mapping docs; no external API doc changes).

## Repository analysis notes (Step 3)

- Target repository: `trustify-backend` (no Serena instance available — analysis performed against the repository structure fixture `repo-backend.md`).
- `CONVENTIONS.md` present at repository root; conventions used: Framework (Axum/SeaORM), Module pattern, Error handling, Response types, Query helpers, Testing.
- Testing readiness template `docs/testing-readiness.md`: **not found** — no testing tasks generated.
- Documentation files discovered: `README.md`, `CONVENTIONS.md` (no `docs/` architecture file in the tree).
- Eval infrastructure: not applicable (no SKILL.md changes).

### Discrepancy flagged

The Feature requirement references `entity/advisory_status.rs` for removal, but the repository structure contains no such file (`entity/src/` lists `advisory.rs`, `sbom.rs`, `sbom_advisory.rs`, `package.rs`, `sbom_package.rs`, `package_license.rs`, `lib.rs`). The lookup table entity/relation may be defined inline in `entity/src/advisory.rs` or the table may exist only in `migration/src/m0001_initial/mod.rs`. Task 3 instructs the implementer to verify and remove any `advisory_status` entity/relation wherever it is actually defined; no non-existent path is listed in Files to Modify.

### Shared-artifact producer / consumer analysis (`advisory.status`)

The advisory status value is a shared artifact read and written across modules.

| Role | Path | Coverage |
|---|---|---|
| Producer (schema + backfill) | `migration/src/m0002_advisory_status_enum/mod.rs` (new), registered in `migration/src/lib.rs` | Task 2 — migration up/down tests |
| Producer (original schema, lookup table definition) | `migration/src/m0001_initial/mod.rs` | Read-only reference for Task 2 (historical migrations are not edited) |
| Producer (ingestion — primary writer) | `modules/ingestor/src/graph/advisory/mod.rs` | Task 5 |
| Producer (ingestion orchestration / on-demand ingest entrypoint) | `modules/ingestor/src/service/mod.rs` | Task 5 |
| Model / entity | `entity/src/advisory.rs`, `entity/src/lib.rs` | Task 3 |
| Consumer (service queries, status filter) | `modules/fundamental/src/advisory/service/advisory.rs` | Task 4 |
| Consumer (response models) | `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/advisory/model/details.rs` | Task 4 |
| Consumer (endpoints) | `modules/fundamental/src/advisory/endpoints/list.rs`, `modules/fundamental/src/advisory/endpoints/get.rs` | Task 4 |
| Consumer (SBOM → advisory views) | `modules/fundamental/src/sbom/service/sbom.rs` | Task 4 (verify/update if it joins `advisory_status`) |
| Consumer (full-text search across entities) | `modules/search/src/service/mod.rs` | Task 4 (verify/update if it joins `advisory_status`) |
| Tests | `tests/api/advisory.rs`, `tests/api/search.rs`, `tests/api/sbom.rs` | Tasks 4, 5 |

No other writers (fallback/recovery or manual API) of advisory status were found in the repository structure — the advisory module exposes only GET endpoints. Task 4 requires a repository-wide grep for `advisory_status` / `status_id` to confirm no additional call sites remain.

## Impact map

```
trustify-backend:
  changes:
    - Add a reversible, atomic migration that creates the `advisory_status_enum` PostgreSQL type (New, Analyzing, Fixed, Rejected), adds `advisory.status`, backfills it from the `status_id` join, drops `advisory.status_id`, and drops the `advisory_status` table
    - Update SeaORM entity definitions: `advisory` entity uses an `AdvisoryStatus` active enum for `status`; remove the `advisory_status` entity/relation
    - Update all advisory queries (service layer, status filter, endpoints, and cross-module consumers in SBOM and search services) to read `advisory.status` directly instead of joining `advisory_status`, keeping the API response shape unchanged
    - Update the advisory ingestion pipeline to map feed status strings to `advisory_status_enum` and write the enum value directly (no lookup-table insert)
    - Update internal architecture documentation to reflect the schema change
```

### Excluded requirements

None — all seven MVP requirements are covered by Tasks 2–5. Non-functional "migration must be tested against a production-sized dataset before deployment" is an operational activity outside the repository; Task 2 includes a verification note but no repository change.

### Risks noted

- **Zero-downtime NFR vs. dropping `status_id`**: the migration drops a column that the currently deployed (old) code reads. Because all changes land together on the feature branch and are deployed as one release, the migration and code ship atomically; however, a rolling deployment where old pods still serve traffic after the migration runs would fail advisory queries. Task 2 Implementation Notes require the migration to run inside a single transaction and recommend the deployment run migrations as part of the same release cutover.
- `ALTER TABLE ... ADD COLUMN` + backfill `UPDATE` takes locks proportional to table size — validate on a production-sized dataset (Customer Considerations).

## Workflow mode decision (Step 4.5)

**Selected mode: `feature-branch`**

Atomicity indicators found:

1. **Coordinated schema migration** — Task 2 drops `advisory.status_id` and the `advisory_status` table; Tasks 3, 4 and 5 change code that reads/writes those objects. Merging the migration alone breaks every advisory query (they join a dropped table).
2. **Cross-cutting refactor / shared type change** — Task 3 changes the `advisory` SeaORM entity (`status_id` → `status: AdvisoryStatus`); Tasks 4 and 5 consume that entity. Merging the entity change without the migration references a non-existent column; merging Tasks 4/5 without Task 3 does not compile.

Interdependent tasks: Task 2 (migration) ↔ Task 3 (entity) ↔ Task 4 (queries) ↔ Task 5 (ingestion). None can land on `main` independently without leaving `main` broken.

Consequences:
- Bookend tasks generated: Task 1 (create branch `TC-9005`), Task 7 (merge `TC-9005` → `main`).
- Intermediate tasks (2–6) target branch `TC-9005`; bookends target `main`.
- Bookend idempotency guard: Feature has no linked issues ("Linked Issues: None") — no existing bookend tasks, generation proceeds.
- The `workflow:feature-branch` label will be added to TC-9005 in Step 6a (existing labels preserved: `ai-generated-jira`, `workflow:feature-branch`).

## Issue types and hierarchy (Step 2.5)

Issue-type discovery is a Jira call and could not be executed in eval mode. CLAUDE.md `## Hierarchy Configuration` sets `Default epic grouping strategy: by-sub-feature`, so the plan assumes a level-1 Epic type exists in project TC:

```
Type-to-role mapping (assumed; to be confirmed via jira.get_project_issue_types):
  Feature: Feature (ID: 10142, level: 2)
  Epic:    Epic    (level: 1)
  Task:    Task    (level: 0)
```

If discovery shows no level-1 type, Epics are skipped and Tasks are linked directly to the Feature (graceful degradation).

### Proposed Epic grouping (by-sub-feature — presented for user approval)

| Epic summary | Tasks |
|---|---|
| TC-9005: Advisory status schema migration | Task 2, Task 3 |
| TC-9005: Advisory query and ingestion updates | Task 4, Task 5 |
| TC-9005: Feature branch delivery and documentation | Task 1, Task 6, Task 7 |

## Task list

| # | Summary | Target Branch | Epic | Depends on |
|---|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | main | Delivery & docs | — |
| 2 | Add advisory status enum migration (create type, backfill, drop FK column and lookup table) | TC-9005 | Schema migration | 1 |
| 3 | Update SeaORM advisory entity to use AdvisoryStatus enum | TC-9005 | Schema migration | 1, 2 |
| 4 | Replace advisory_status joins with advisory.status column in queries and endpoints | TC-9005 | Query & ingestion | 1, 3 |
| 5 | Write advisory status enum directly in ingestion pipeline | TC-9005 | Query & ingestion | 1, 3 |
| 6 | Update internal architecture documentation for advisory status enum | TC-9005 | Delivery & docs | 1, 2, 3, 4, 5 |
| 7 | Merge feature branch TC-9005 to main | main | Delivery & docs | 1, 2, 3, 4, 5, 6 |

## `additional_fields` for created issues (Step 6a / 6a.0)

Applied to all three Epics and all seven Tasks:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

- priority: inherited from Feature ("High", not "Undefined") — propagated
- fixVersions: Feature has `RHTPA 2.0.0`; `fixVersion scope: both` — propagated
- Task `parent`: assigned Epic key (see task-creation-log.md)
- Feature TC-9005: `labels` → `["ai-generated-jira", "workflow:feature-branch"]`

See `task-creation-log.md` for the full creation sequence, links, and digests.
