## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` column. The Feature's Documentation Considerations indicate a minor doc impact: internal architecture docs need updating to reflect the schema change. No external API documentation changes are needed since the response shape remains identical.

Documentation scope (from Feature TC-9005 Documentation Considerations):
- **Doc impact type**: Updates to existing content
- **Details**: Update internal architecture docs to reflect schema change; SeaORM enum mapping documentation for reference
- **No external API changes**: The response shape remains identical (status is still a string)

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new schema: `advisory.status` is an `advisory_status_enum` column, not a foreign key to `advisory_status`
- [ ] Documentation references to the `advisory_status` lookup table are removed or updated
- [ ] SeaORM enum mapping pattern is documented for future reference
- [ ] No references to the old `status_id` foreign key pattern remain in documentation

## Test Requirements
- [ ] Verify documentation accurately describes the current database schema after migration
- [ ] Verify documentation is consistent with the implemented enum column approach
- [ ] Verify no stale references to the `advisory_status` table remain in any documentation files

## Dependencies
- Depends on: Task 4 -- Update advisory service and endpoints to use enum column
- Depends on: Task 5 -- Update advisory ingestion pipeline
- Depends on: Task 6 -- Database migration to drop status_id and advisory_status table
