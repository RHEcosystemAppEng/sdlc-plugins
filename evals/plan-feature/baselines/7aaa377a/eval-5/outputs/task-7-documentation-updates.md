## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The documentation impact is minor — no external API documentation changes are needed since the response shape remains identical (status is still a string). Updates should cover the internal data model change, the rationale for the migration (eliminating join overhead, reducing schema complexity), and reference SeaORM enum mapping documentation for developers working with the new schema.

Doc impact type: Updates to existing content.

Reference: Feature TC-9005 — Drop status table and migrate to enum column.

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new schema (enum column instead of lookup table)
- [ ] Documentation explains the rationale for the migration
- [ ] SeaORM enum mapping patterns are referenced for developer guidance
- [ ] No inaccurate references to the `advisory_status` lookup table remain in documentation

## Test Requirements
- [ ] Documentation is accurate and consistent with the implemented schema changes
- [ ] Documentation covers the scope identified in Documentation Considerations (internal architecture docs)

## Dependencies
- Depends on: Task 4 — Update advisory service and model to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline for enum status
- Depends on: Task 6 — Update advisory integration tests
