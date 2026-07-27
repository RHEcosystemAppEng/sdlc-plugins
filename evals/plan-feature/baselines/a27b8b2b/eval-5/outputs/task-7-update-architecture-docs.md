## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column. The documentation should describe the new schema structure, the rationale for the migration (performance improvement, reduced complexity), and the mapping of status values. No external API documentation changes are needed since the API response shape is unchanged.

This task addresses the Documentation Considerations from the Feature description:
- Doc impact type: Updates to existing content
- Scope: Internal architecture docs reflecting the schema change
- Reference material: SeaORM enum mapping documentation

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new `advisory_status_enum` column on the `advisory` table
- [ ] Documentation describes the four status values (New, Analyzing, Fixed, Rejected) and their usage
- [ ] Documentation notes that the `advisory_status` lookup table has been removed
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documentation accurately describes the current schema (enum column, not lookup table)
- [ ] Verify documentation does not reference the removed `advisory_status` table as if it still exists
- [ ] Verify no broken internal links or references

## Dependencies
- Depends on: Task 2 — Create migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update advisory ingestion pipeline
