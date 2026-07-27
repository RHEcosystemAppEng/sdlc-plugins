## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to a PostgreSQL enum column on the `advisory` table. The feature's Documentation Considerations indicate minor doc impact: update internal architecture docs to reflect the schema change. No external API documentation changes are needed since the API response shape is unchanged.

Doc impact type: Updates to existing content
Details: Update internal architecture docs to reflect the schema change from lookup table to enum column. Reference SeaORM enum mapping documentation for the new entity pattern.

Reference: Feature TC-9005 — Drop status table and migrate to enum column

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new schema (enum column instead of lookup table)
- [ ] Documentation covers the SeaORM enum mapping pattern used for advisory status
- [ ] No references to the `advisory_status` lookup table remain in documentation

## Test Requirements
- [ ] Documentation accurately describes the current schema after the migration
- [ ] Documentation is consistent with the implemented feature behavior

## Dependencies
- Depends on: Task 2 — Database migration
- Depends on: Task 3 — Update SeaORM entity definitions
- Depends on: Task 4 — Update advisory service and model layer
- Depends on: Task 5 — Update advisory endpoints
- Depends on: Task 6 — Update advisory ingestion pipeline
- Depends on: Task 7 — Update integration tests
