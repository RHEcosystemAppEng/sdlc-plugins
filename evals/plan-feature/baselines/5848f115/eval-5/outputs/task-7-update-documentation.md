## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The documentation should describe the new schema design, the rationale for the migration (eliminating unnecessary join overhead, simplifying queries), and the enum values (New, Analyzing, Fixed, Rejected). No external API documentation changes are needed since the API response shape is unchanged.

Documentation impact type: Updates to existing content.
Details: Minor update to internal architecture docs reflecting the schema change. Reference material includes SeaORM enum mapping documentation.
Feature reference: TC-9005 — Drop status table and migrate to enum column.

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new advisory status schema (enum column instead of lookup table)
- [ ] The documentation covers the enum type and its four values
- [ ] No references to the `advisory_status` lookup table as a current schema element remain in documentation (historical references are acceptable)

## Test Requirements
- [ ] Verify the documentation is accurate, complete, and consistent with the implemented feature behavior
- [ ] Verify that the schema description matches the actual database structure after migration

## Dependencies
- Depends on: Task 4 — Update advisory service and endpoint queries
- Depends on: Task 5 — Update advisory ingestion pipeline
