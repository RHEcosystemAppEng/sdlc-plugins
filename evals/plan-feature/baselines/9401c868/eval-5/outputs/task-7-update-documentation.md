## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to a PostgreSQL enum column on the `advisory` table. The doc impact type is "Updates to existing content" as identified in the Feature's Documentation Considerations section (TC-9005).

Changes to document:
- The `advisory` table now uses an `advisory_status_enum` PostgreSQL enum column (`status`) instead of a foreign key (`status_id`) to the `advisory_status` lookup table
- The `advisory_status` lookup table has been dropped from the schema
- Advisory queries no longer require a join for status information, improving p95 latency
- The ingestion pipeline writes enum values directly to the advisory row
- SeaORM entity definitions use `DeriveActiveEnum` for the status enum mapping

No external API documentation changes are needed -- the response shape remains identical (status is still a string).

Reference material: SeaORM enum mapping documentation.

## Acceptance Criteria
- [ ] Architecture documentation accurately reflects the enum-based advisory status schema
- [ ] Documentation mentions the removal of the `advisory_status` lookup table
- [ ] Documentation describes the `advisory_status_enum` type and its four values (New, Analyzing, Fixed, Rejected)
- [ ] Documentation reflects the simplified query pattern (no join required for status)
- [ ] No stale references to the old `advisory_status` join pattern remain in documentation

## Test Requirements
- [ ] Documentation is accurate, complete, and consistent with the implemented feature behavior
- [ ] All code references in documentation (file paths, type names, query patterns) match the current codebase after implementation

## Dependencies
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum values
- Depends on: Task 6 -- Update advisory integration tests for status enum
