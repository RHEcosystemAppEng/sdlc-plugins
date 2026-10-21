## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The documentation should describe the new schema design, the rationale for the migration (eliminating unnecessary join overhead, simplifying queries), and the current set of valid status values (New, Analyzing, Fixed, Rejected).

The doc impact type is "Updates to existing content" per the feature's Documentation Considerations section. No external API documentation changes are needed since the API response shape remains identical.

Reference material: SeaORM enum mapping documentation.

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new `advisory.status` enum column
- [ ] Documentation describes the rationale for replacing the lookup table with an enum
- [ ] Documentation lists the valid enum values (New, Analyzing, Fixed, Rejected)
- [ ] No references to the deprecated `advisory_status` lookup table remain in documentation (unless in migration history context)

## Test Requirements
- [ ] Documentation is accurate and consistent with the implemented feature behavior
- [ ] Documentation covers the scope identified in the Feature's Documentation Considerations section

## Dependencies
- Depends on: Task 4 — Update advisory service and endpoint queries to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
