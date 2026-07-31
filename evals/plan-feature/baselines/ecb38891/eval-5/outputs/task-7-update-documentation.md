## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The documentation impact is minor -- no external API documentation changes are needed since the API response shape remains identical (status is still returned as a string). Updates should focus on internal architecture docs and schema documentation.

**Doc impact type:** Updates to existing content
**Details:** Update internal architecture docs to reflect schema change. Reference SeaORM enum mapping documentation for the new entity pattern. No user-facing API documentation changes needed.
**Feature reference:** TC-9005 -- Drop status table and migrate to enum column

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new enum-based advisory status schema
- [ ] Documentation describes the `advisory_status_enum` PostgreSQL type and its four values
- [ ] Documentation notes that the `advisory_status` lookup table has been removed
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documentation accurately describes the current schema (enum column, not FK join)
- [ ] Verify no references to the removed `advisory_status` lookup table remain in documentation

## Dependencies
- Depends on: Task 4 -- Update advisory service layer and endpoints
- Depends on: Task 5 -- Update advisory ingestion pipeline
