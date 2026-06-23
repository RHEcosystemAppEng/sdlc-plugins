# Repository Impact Map

## Feature
**TC-9005**: Drop status table and migrate to enum column

## Workflow Mode Decision

**Selected mode**: feature-branch

**Rationale**: This feature requires feature-branch workflow because multiple atomicity indicators are present:

1. **Coordinated schema migrations**: The database migration creates an enum type, adds a column, backfills data, drops a foreign key, and drops a table -- all of which must land atomically. A partial migration (enum column exists but lookup table already dropped, or vice versa) would leave the database in an inconsistent state.
2. **Tightly coupled components**: The migration, entity definitions, service layer, endpoints, and ingestion pipeline are all interdependent. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist.
3. **Cross-cutting refactors**: Every advisory query across the service layer, endpoints, and ingestion pipeline must be updated to use the new enum column instead of the join -- changes span multiple modules that must be coordinated.

The non-functional requirements explicitly state: "All changes must land together" and "Migration must be atomic." These are definitive atomicity constraints.

A `workflow:feature-branch` label should be applied to the feature issue TC-9005.

## Impacted Repository

### trustify-backend

| Area | Impact | Key Files |
|---|---|---|
| Database migrations | New migration to create enum type, add column, backfill, drop FK column, drop lookup table | `migration/src/` (new migration module) |
| Entity definitions | Update advisory entity to use enum column; remove advisory_status entity | `entity/src/advisory.rs`, `entity/src/lib.rs` |
| Advisory service | Update all queries to use enum column instead of join | `modules/fundamental/src/advisory/service/advisory.rs` |
| Advisory model | Update summary/details structs to source status from enum column | `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/advisory/model/details.rs` |
| Advisory endpoints | Update list and get endpoints (query changes flow through service) | `modules/fundamental/src/advisory/endpoints/list.rs`, `modules/fundamental/src/advisory/endpoints/get.rs` |
| Ingestion pipeline | Write enum values directly instead of lookup table insert | `modules/ingestor/src/graph/advisory/mod.rs` |
| Integration tests | Update advisory tests to reflect new schema | `tests/api/advisory.rs` |

## Task Sequence

| Task | Summary | Target Branch | Dependencies |
|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | main | None |
| 2 | Create database migration for advisory status enum | TC-9005 | Task 1 |
| 3 | Update SeaORM entity definitions for advisory status enum | TC-9005 | Task 1 |
| 4 | Update advisory service and endpoints to use status enum column | TC-9005 | Task 1 |
| 5 | Update advisory ingestion pipeline to write enum status directly | TC-9005 | Task 1 |
| 6 | Update advisory integration tests for status enum migration | TC-9005 | Task 1 |
| 7 | Merge feature branch TC-9005 to main | main | Tasks 2, 3, 4, 5, 6 |
