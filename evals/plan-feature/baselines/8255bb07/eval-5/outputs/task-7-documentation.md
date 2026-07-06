## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The Feature's Documentation Considerations indicate minor doc impact -- update internal architecture docs to reflect the schema change. No external API documentation changes are needed since the response shape remains identical.

Doc impact type: Updates to existing content
Reference material: SeaORM enum mapping documentation

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new `advisory_status_enum` column schema
- [ ] Documentation describes the rationale for migrating from the lookup table to enum column
- [ ] No references to the removed `advisory_status` table remain in documentation
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documentation accurately describes the new schema structure
- [ ] Verify documentation does not reference the removed `advisory_status` lookup table
- [ ] Verify documentation is complete and consistent with the implemented changes

## Dependencies
- Depends on: Task 4 -- Update advisory service, models, and endpoints to use status enum
- Depends on: Task 5 -- Update advisory ingestion pipeline for status enum
- Depends on: Task 6 -- Update advisory integration tests for status enum
