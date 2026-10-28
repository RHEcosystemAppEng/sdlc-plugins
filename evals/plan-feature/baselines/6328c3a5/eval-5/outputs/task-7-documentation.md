## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the advisory status schema change. The `advisory_status` lookup table has been replaced by a PostgreSQL enum column (`advisory_status_enum`) directly on the `advisory` table. This is an internal documentation update -- no external API documentation changes are needed since the response shape remains identical.

**Doc impact type**: Updates to existing content
**Feature reference**: TC-9005 -- Drop status table and migrate to enum column

Documentation should cover:
- The schema change from lookup table to enum column
- The rationale for the change (performance improvement, reduced schema complexity)
- The enum values (New, Analyzing, Fixed, Rejected)
- Reference to SeaORM enum mapping documentation

## Acceptance Criteria
- [ ] Architecture documentation accurately reflects the new enum-based advisory status schema
- [ ] Documentation explains the rationale for the schema change
- [ ] Documentation lists the valid enum values
- [ ] No references to the old `advisory_status` lookup table remain in documentation

## Test Requirements
- [ ] Documentation is accurate and consistent with the implemented schema change
- [ ] Documentation correctly describes the enum type and its values

## Dependencies
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum column
- Depends on: Task 5 -- Update advisory ingestion pipeline for direct enum writes
