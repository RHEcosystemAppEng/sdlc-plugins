## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to a direct `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The feature's Documentation Considerations indicate a minor doc impact: internal architecture docs need updating to reflect the schema change, but no external API documentation changes are needed. Reference SeaORM enum mapping documentation for the new entity pattern.

This is a documentation-only task. No code changes are required.

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new schema: `advisory.status` is an enum column of type `advisory_status_enum`, not a foreign key to a lookup table
- [ ] Documentation covers the enum values: New, Analyzing, Fixed, Rejected
- [ ] No references to the `advisory_status` lookup table remain in documentation (unless describing the migration history)
- [ ] SeaORM enum mapping pattern is documented or referenced for the `AdvisoryStatusEnum` entity definition

## Test Requirements
- [ ] Verify documentation accurately describes the current schema after migration
- [ ] Verify documentation is consistent with the implemented entity definition in `entity/src/advisory.rs`

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum conversion
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use status enum column
- Depends on: Task 5 — Update advisory ingestion pipeline for direct enum writes
- Depends on: Task 6 — Update integration tests for advisory status enum
