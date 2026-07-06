## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The feature's Documentation Considerations indicate a minor doc impact: internal architecture docs need updating to reflect the schema change. No external API documentation changes are needed since the response shape remains identical.

Doc impact type: Updates to existing content.

Details:
- Update internal architecture docs to reflect that advisory status is stored as a PostgreSQL enum column (`advisory.status`) rather than a separate lookup table (`advisory_status`)
- Reference SeaORM enum mapping documentation for the new entity pattern
- No user-facing API documentation changes required (response shape is unchanged)

Reference: Feature TC-9005 — Drop status table and migrate to enum column.

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new `advisory_status_enum` schema
- [ ] Documentation describes the migration from lookup table to enum column
- [ ] Documentation references the `AdvisoryStatusEnum` entity pattern
- [ ] No references to the removed `advisory_status` lookup table remain in architecture docs

## Test Requirements
- [ ] Verify documentation accurately describes the current schema (enum column, not lookup table)
- [ ] Verify documentation is consistent with the implemented entity definitions in `entity/src/advisory.rs`
- [ ] Verify no stale references to `advisory_status` table remain

## Dependencies
- Depends on: Task 4 — Update advisory service layer and endpoints to use status enum
- Depends on: Task 5 — Update advisory ingestion pipeline for status enum
- Depends on: Task 6 — Update advisory integration tests for status enum
