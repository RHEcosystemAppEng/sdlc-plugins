## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the advisory status schema change from a lookup table (`advisory_status`) to a PostgreSQL enum column (`advisory_status_enum`) on the `advisory` table. The feature TC-9005 removes the `advisory_status` table and replaces the `status_id` foreign key with a direct `status` enum column, simplifying queries and reducing join overhead.

Doc impact type: Updates to existing content.
Details: Internal architecture docs need updating to reflect the schema simplification. No external API documentation changes are needed since the response shape is unchanged. Reference material: SeaORM enum mapping documentation.

Reference: Feature TC-9005 — Drop status table and migrate to enum column.

## Acceptance Criteria
- [ ] Internal architecture documentation accurately describes the new schema (enum column instead of lookup table)
- [ ] Documentation covers the `advisory_status_enum` type and its four values (New, Analyzing, Fixed, Rejected)
- [ ] Any entity relationship diagrams or schema descriptions are updated to remove the `advisory_status` table
- [ ] Documentation notes that the API response shape is unchanged

## Test Requirements
- [ ] Verify documentation accurately reflects the implemented schema change
- [ ] Verify no references to the dropped `advisory_status` table remain in architecture docs
- [ ] Verify documentation is consistent with the actual entity definitions and migration

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use status enum
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 — Update advisory integration tests
