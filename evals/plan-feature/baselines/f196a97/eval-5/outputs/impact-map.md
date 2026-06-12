# Repository Impact Map

## Feature: TC-9005 — Drop status table and migrate to enum column

```
trustify-backend:
  changes:
    - Create database migration to define advisory_status_enum PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
    - Add status enum column to advisory table and backfill from existing status_id join
    - Drop status_id foreign key column from advisory table
    - Drop advisory_status lookup table
    - Update SeaORM advisory entity (entity/advisory.rs) to replace status_id foreign key with status enum column
    - Remove SeaORM advisory_status entity file (entity/advisory_status.rs is no longer needed — but since the repo fixture does not list it, remove references from entity/lib.rs)
    - Update AdvisoryService (modules/fundamental/src/advisory/service/advisory.rs) to query status column directly instead of joining advisory_status
    - Update AdvisorySummary and AdvisoryDetails models (modules/fundamental/src/advisory/model/) to use enum status field instead of joined status
    - Update advisory list endpoint (modules/fundamental/src/advisory/endpoints/list.rs) to filter by enum status column
    - Update advisory get endpoint (modules/fundamental/src/advisory/endpoints/get.rs) to return status from enum column
    - Update advisory ingestion pipeline (modules/ingestor/src/graph/advisory/mod.rs) to write enum values directly instead of lookup table insert
    - Update advisory integration tests (tests/api/advisory.rs) to use new status column
```

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migration** — The database migration adds the `advisory_status_enum` type and `status` column that all code changes depend on. Merging the migration without the code changes would leave queries joining a dropped table. Merging the code changes without the migration would reference a column that does not exist.

2. **All-or-nothing delivery requirement** — The feature's non-functional requirements explicitly state: "All changes must land together: merging the migration without the code changes would break all advisory queries, and merging the code changes without the migration would reference a column that does not exist."

3. **Cross-cutting refactor** — The status column change spans the entity layer, service layer, endpoint layer, ingestion pipeline, and tests. Partial delivery would leave the codebase in an inconsistent state where some queries use the join and others reference the nonexistent enum column.

**Interdependent tasks:** All implementation tasks are interdependent. The migration must exist before entity/service/endpoint/ingestion changes can work, and the entity changes must exist before service/endpoint changes compile. All must be merged together.
