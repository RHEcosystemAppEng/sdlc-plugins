# Task 9 — Update documentation for advisory schema change

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the advisory status schema change from a lookup table to a PostgreSQL enum column. The Feature's Documentation Considerations indicate minor doc impact: update existing internal architecture docs to reflect the schema change. No external API documentation changes are needed, as the API response shape is unchanged (status remains a string).

Doc impact type: Updates to existing content.

Reference material: SeaORM enum mapping documentation.

Reference: Feature TC-9005 — Drop status table and migrate to enum column.

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new advisory status enum schema
- [ ] Documentation describes the `advisory_status_enum` PostgreSQL type and its four values (New, Analyzing, Fixed, Rejected)
- [ ] No documentation references the removed `advisory_status` lookup table as if it still exists
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documentation accurately describes the current schema after migration
- [ ] Verify no stale references to `advisory_status` table remain in documentation files

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum conversion
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 5 — Update advisory service to eliminate status table join
- Depends on: Task 6 — Update advisory endpoints for enum status filtering
- Depends on: Task 7 — Update advisory ingestion pipeline for direct enum writes
- Depends on: Task 8 — Update advisory integration tests for new schema
