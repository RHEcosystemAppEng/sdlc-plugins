## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. Document the new enum type, the simplified query pattern (no join required), and the migration approach for reference. No external API documentation changes are needed since the response shape is unchanged.

## Acceptance Criteria
- [ ] Internal architecture docs reflect that `advisory.status` is now an enum column, not a foreign key to a lookup table
- [ ] The `advisory_status` lookup table is documented as removed
- [ ] The `advisory_status_enum` PostgreSQL type is documented with its values (New, Analyzing, Fixed, Rejected)
- [ ] Query pattern documentation reflects the elimination of the status join

## Test Requirements
- [ ] Verify documentation is consistent with the implemented schema changes
- [ ] Verify no references to the removed `advisory_status` table remain in architecture docs

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service, model, and endpoints to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
