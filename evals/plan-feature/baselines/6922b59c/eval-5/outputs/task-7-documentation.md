## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the advisory status schema change from a lookup table to a PostgreSQL enum column. The feature (TC-9005) replaces the `advisory_status` lookup table with an `advisory_status_enum` type and a `status` column directly on the `advisory` table.

Documentation impact type: Updates to existing content. The feature's Documentation Considerations section indicates minor internal architecture doc updates are needed. No external API documentation changes are required since the response shape remains identical.

Reference: Feature TC-9005 — Drop status table and migrate to enum column.

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new schema: `advisory.status` is a PostgreSQL enum column, not a foreign key to a lookup table
- [ ] Any data model diagrams or ERD references are updated to remove the `advisory_status` table and the `status_id` foreign key
- [ ] Documentation notes that the four advisory status values (New, Analyzing, Fixed, Rejected) are defined as a PostgreSQL enum type
- [ ] No references to the `advisory_status` lookup table remain in architecture documentation

## Test Requirements
- [ ] Verify documentation accurately describes the enum-based status schema
- [ ] Verify no stale references to the `advisory_status` lookup table remain in documentation files

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline for enum values
- Depends on: Task 6 — Update advisory integration tests
