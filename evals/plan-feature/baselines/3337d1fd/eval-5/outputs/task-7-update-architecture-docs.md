## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to an `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The Feature's Documentation Considerations indicate minor doc impact — internal architecture docs need updating, but no external API documentation changes are required since the response shape remains identical.

Doc impact type: Updates to existing content. The documentation should cover: the removal of the `advisory_status` table, the addition of the `advisory_status_enum` type, the updated `advisory.status` column, and the simplified query pattern (no join required for status filtering).

Reference: Feature TC-9005 — Drop status table and migrate to enum column.

## Acceptance Criteria
- [ ] Architecture documentation reflects the new `advisory_status_enum` column instead of the `advisory_status` lookup table
- [ ] Documentation accurately describes the simplified query pattern (direct column access, no join)
- [ ] No references to the `advisory_status` lookup table remain in architecture docs
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documentation accurately reflects the schema change
- [ ] Verify documentation is consistent with the SeaORM entity definitions in `entity/src/advisory.rs`
- [ ] Verify no stale references to the `advisory_status` table remain in docs

## Dependencies
- Depends on: Task 4 — Update advisory service, model, and endpoint layers
- Depends on: Task 5 — Update advisory ingestion pipeline
