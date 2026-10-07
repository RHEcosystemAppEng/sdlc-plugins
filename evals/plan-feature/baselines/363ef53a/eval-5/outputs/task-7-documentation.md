## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The feature eliminates a join-based status lookup in favor of a direct enum column, simplifying queries and improving advisory list endpoint performance.

Doc impact type: Updates to existing content

Documentation considerations from the feature:
- Minor impact -- update internal architecture docs to reflect schema change
- No external API documentation changes needed
- Reference material: SeaORM enum mapping documentation

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new schema (enum column replaces lookup table)
- [ ] Documentation covers the rationale for the migration (performance improvement, reduced complexity)
- [ ] No references to the dropped `advisory_status` table remain in documentation
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Documentation accurately describes the `advisory_status_enum` type and its four values (New, Analyzing, Fixed, Rejected)
- [ ] Documentation reflects the simplified query pattern (direct column access, no join)
- [ ] Documentation is internally consistent -- no contradictions between schema description and code references

## Dependencies
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum
- Depends on: Task 5 -- Update advisory ingestion pipeline for direct enum writes
- Depends on: Task 6 -- Update advisory integration tests for status enum
