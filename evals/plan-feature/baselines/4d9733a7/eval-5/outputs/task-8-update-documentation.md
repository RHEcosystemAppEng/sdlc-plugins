## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to a PostgreSQL enum column on the `advisory` table. The Feature's Documentation Considerations indicate this is a minor doc impact — internal architecture docs need updating, but no external API documentation changes are required.

Doc impact type: Updates to existing content
Details: Update internal architecture docs to reflect schema change. Reference material includes SeaORM enum mapping documentation. No external API documentation changes needed since the response shape remains identical.

Reference: Feature TC-9005 — Drop status table and migrate to enum column

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new schema: `advisory.status` enum column replaces the `advisory_status` lookup table and `status_id` FK
- [ ] Documentation describes the `advisory_status_enum` type and its valid values (New, Analyzing, Fixed, Rejected)
- [ ] No references to the `advisory_status` lookup table remain in documentation (except as historical context if appropriate)
- [ ] Documentation covers the scope identified in Documentation Considerations: schema change, no external API impact

## Test Requirements
- [ ] Verify documentation is accurate and consistent with the implemented schema change
- [ ] Verify no stale references to the old `advisory_status` table exist in documentation

## Dependencies
- Depends on: Task 2 — Add database migration for advisory status enum conversion
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and model layer to use enum status
- Depends on: Task 5 — Update advisory REST endpoints for enum status filtering
- Depends on: Task 6 — Update advisory ingestion pipeline for direct enum writes
- Depends on: Task 7 — Update advisory integration tests for enum status
