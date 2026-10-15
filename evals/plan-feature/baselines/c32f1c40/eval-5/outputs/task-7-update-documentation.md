## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The documentation changes should cover:

- The rationale for the migration (eliminating join overhead, simplifying queries)
- The new schema structure (enum column replaces lookup table and FK)
- The enum values (New, Analyzing, Fixed, Rejected)
- Any SeaORM-specific patterns used for enum mapping (`DeriveActiveEnum`)

**Doc impact type:** Updates to existing content
**Details:** Minor internal documentation update. No external API documentation changes are needed since the API response shape is unchanged.

Reference: Feature TC-9005

## Acceptance Criteria
- [ ] Internal architecture documentation accurately describes the new advisory status schema
- [ ] Documentation reflects that the `advisory_status` lookup table has been removed
- [ ] Documentation describes the `advisory_status_enum` type and its values
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documentation accurately describes the new schema structure
- [ ] Verify documentation does not reference the removed `advisory_status` lookup table as current
- [ ] Verify documentation is complete and covers the migration rationale

## Dependencies
- Depends on: Task 2 -- Create advisory status enum migration
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum
- Depends on: Task 5 -- Update advisory ingestion pipeline for status enum
- Depends on: Task 6 -- Update advisory integration tests
