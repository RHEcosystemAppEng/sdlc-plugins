# Repository Impact Map — TC-9005

## Feature
**TC-9005**: Drop status table and migrate to enum column

## Workflow Mode Decision

**Mode**: `feature-branch`

**Rationale**: The feature's Non-Functional Requirements explicitly state three atomicity constraints that require all changes to land together:

1. "Migration must be atomic: if any step fails, the entire migration rolls back" — the database migration (enum type creation, column addition, backfill, FK drop, table drop) must succeed or fail as a unit.
2. "All changes must land together: merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist" — a partial merge of any task to main would leave the application in a broken state.
3. "Zero downtime: migration must be safe to run while the application is serving traffic" — the migration and code changes must be coordinated to avoid downtime.

These constraints mean individual tasks cannot safely merge to main independently. A feature branch collects all changes, and a single merge to main ensures atomicity.

**Label**: `workflow:feature-branch`

## Impacted Repository

### trustify-backend

| Area | Impact | Files |
|---|---|---|
| Database migration | New migration to create enum type, add column, backfill, drop FK, drop table | `migration/src/` (new migration module) |
| Entity definitions | Update advisory entity to use enum column; remove advisory_status entity | `entity/src/advisory.rs`, `entity/src/lib.rs` |
| Advisory model | Update AdvisorySummary and AdvisoryDetails to use enum status | `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/advisory/model/details.rs`, `modules/fundamental/src/advisory/model/mod.rs` |
| Advisory service | Remove status join from advisory queries | `modules/fundamental/src/advisory/service/advisory.rs` |
| Advisory endpoints | Update list and get endpoints for new status column | `modules/fundamental/src/advisory/endpoints/list.rs`, `modules/fundamental/src/advisory/endpoints/get.rs` |
| Ingestion pipeline | Write enum values directly instead of lookup table | `modules/ingestor/src/graph/advisory/mod.rs` |
| Integration tests | Update advisory endpoint tests | `tests/api/advisory.rs` |

## Task Summary

| Task | Summary | Target Branch |
|---|---|---|
| 1 | Create feature branch TC-9005 from main | main |
| 2 | Create database migration for advisory status enum | TC-9005 |
| 3 | Update SeaORM entity definitions for advisory status enum | TC-9005 |
| 4 | Update advisory service and model layer to use status enum | TC-9005 |
| 5 | Update advisory ingestion pipeline for direct enum writes | TC-9005 |
| 6 | Update advisory endpoints and integration tests | TC-9005 |
| 7 | Merge feature branch TC-9005 to main | main |
