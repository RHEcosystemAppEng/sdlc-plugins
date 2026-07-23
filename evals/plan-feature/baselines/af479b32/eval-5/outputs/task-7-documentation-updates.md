# Task 7: Update internal architecture documentation for advisory status enum migration

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to a PostgreSQL enum column on the `advisory` table. The Feature's Documentation Considerations identify this as a minor doc update -- internal architecture docs need to reflect the new schema, but no external API documentation changes are needed since the API response shape is unchanged.

The documentation should cover:
- The new `advisory_status_enum` PostgreSQL type and its values
- The simplified advisory query pattern (no join required for status)
- The removal of the `advisory_status` lookup table
- Reference to SeaORM enum mapping documentation for future maintainers

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new advisory status enum schema
- [ ] Documentation explains the rationale for the migration (performance, simplicity)
- [ ] Documentation notes the four valid status values (New, Analyzing, Fixed, Rejected)
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documentation accurately describes the current schema after migration
- [ ] Verify documentation does not reference the removed `advisory_status` lookup table as current architecture
- [ ] Verify documentation is complete -- covers enum type, column, and query pattern changes

## Dependencies
- Depends on: Task 4 -- Update advisory service layer and endpoints to use status enum column
- Depends on: Task 5 -- Update advisory ingestion pipeline for direct enum writes
- Depends on: Task 6 -- Update advisory integration tests for status enum
