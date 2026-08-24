## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the advisory schema change from a lookup table (`advisory_status`) to a PostgreSQL enum column (`advisory.status`). The feature TC-9005 eliminates the `advisory_status` table and replaces it with an `advisory_status_enum` type. Documentation should reflect the simplified data model, updated query patterns, and the rationale for the migration.

Doc impact type: Updates to existing content.

Reference feature: TC-9005 — Drop status table and migrate to enum column.

## Acceptance Criteria
- [ ] Architecture documentation accurately describes the new advisory schema with the `status` enum column
- [ ] Documentation no longer references the `advisory_status` lookup table as a current schema element
- [ ] The rationale for the migration (performance, simplicity) is documented
- [ ] SeaORM enum mapping pattern is documented or referenced

## Test Requirements
- [ ] Verify documentation is accurate and consistent with the implemented schema change
- [ ] Verify no stale references to the `advisory_status` table remain in documentation

## Dependencies
- Depends on: Task 4 — Update advisory service and endpoint queries to use enum status
- Depends on: Task 5 — Update advisory ingestion pipeline for enum status
- Depends on: Task 6 — Update advisory integration tests for enum status
