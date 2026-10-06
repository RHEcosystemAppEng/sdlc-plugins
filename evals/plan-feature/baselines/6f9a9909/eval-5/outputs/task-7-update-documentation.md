# Task 7 — Update internal architecture documentation

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The Feature's Documentation Considerations indicate a minor doc impact: update internal architecture docs to reflect the schema change. No external API documentation changes are needed since the response shape remains identical.

**Doc impact type:** Updates to existing content

**Details:**
- Update any architecture diagrams or schema descriptions that reference the `advisory_status` lookup table and the `advisory.status_id` foreign key relationship
- Document the new `advisory_status_enum` PostgreSQL type and the `advisory.status` column
- Reference SeaORM enum mapping documentation as applicable
- No user-facing API documentation changes needed (response shape is unchanged)

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new schema (enum column instead of lookup table)
- [ ] Any entity-relationship diagrams or schema descriptions are updated to show `advisory.status` as an enum column
- [ ] Documentation mentions the four enum values: `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] No documentation references the removed `advisory_status` table or `status_id` FK column as current schema

## Test Requirements
- [ ] Verify documentation accurately describes the current schema after migration
- [ ] Verify no stale references to `advisory_status` table remain in documentation
- [ ] Verify documentation is consistent with the implemented feature behavior

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum conversion
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status
- Depends on: Task 4 — Update advisory service and endpoints for enum status
- Depends on: Task 5 — Update advisory ingestion pipeline for enum status
- Depends on: Task 6 — Update advisory integration tests for enum status
