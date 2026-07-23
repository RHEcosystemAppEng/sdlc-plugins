## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The Feature's Documentation Considerations indicate a minor documentation impact: internal architecture docs need updating to reflect the schema change, but no external API documentation changes are needed since the API response shape is unchanged.

Documentation should cover:
- The removal of the `advisory_status` lookup table from the schema
- The addition of the `advisory_status_enum` PostgreSQL enum type
- The new `status` enum column on the `advisory` table
- The simplified query path (no join required for status filtering)

Doc impact type: Updates to existing content
Reference material: SeaORM enum mapping documentation

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new schema (enum column, no lookup table)
- [ ] Documentation covers the rationale for the change (performance improvement, reduced complexity)
- [ ] No references to the `advisory_status` lookup table remain in documentation as current architecture

## Test Requirements
- [ ] Verify documentation is consistent with the implemented schema changes
- [ ] Verify no stale references to the old lookup table pattern

## Dependencies
- Depends on: Task 2 -- Create migration for advisory_status_enum
- Depends on: Task 3 -- Update SeaORM entity definitions
- Depends on: Task 5 -- Update AdvisoryService
- Depends on: Task 6 -- Update advisory endpoints
- Depends on: Task 7 -- Update ingestion pipeline
- Depends on: Task 8 -- Update integration tests
