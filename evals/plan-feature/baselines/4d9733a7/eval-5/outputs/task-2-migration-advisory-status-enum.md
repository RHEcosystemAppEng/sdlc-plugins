## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that converts the `advisory_status` lookup table into a PostgreSQL enum column on the `advisory` table. The migration must:

1. Create a PostgreSQL enum type `advisory_status_enum` with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the new `status` column from the existing `advisory_status` table via the `status_id` foreign key join
4. Drop the `status_id` foreign key column from the `advisory` table
5. Drop the `advisory_status` lookup table

The migration must be atomic (all steps in a single migration) and reversible (the down migration recreates the lookup table, re-adds the FK column, and backfills from the enum column).

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration list

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration implementing enum type creation, column addition, data backfill, FK column drop, and lookup table drop

## Implementation Notes
- Use SeaORM's migration framework (`MigrationTrait`) for the up/down implementations. The existing migration at `migration/src/m0001_initial/mod.rs` demonstrates the established pattern.
- The backfill step should use a single SQL statement: `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum` to avoid row-by-row processing.
- The down migration must reverse all steps: recreate `advisory_status` table, re-add `status_id` column, backfill from enum, drop `status` column, drop enum type.
- For zero-downtime safety, the migration should be structured so that the enum column is added and backfilled before the FK column is dropped, ensuring data integrity throughout.
- Per CONVENTIONS.md §Framework: use SeaORM migration framework for all schema changes.
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's Rust migration file scope.

## Acceptance Criteria
- [ ] The `advisory_status_enum` PostgreSQL enum type exists with values (New, Analyzing, Fixed, Rejected)
- [ ] The `advisory` table has a `status` column of type `advisory_status_enum`
- [ ] All existing advisory rows have their `status` column populated from the former `status_id` join
- [ ] The `status_id` column no longer exists on the `advisory` table
- [ ] The `advisory_status` table no longer exists
- [ ] The migration is reversible: running `down` restores the previous schema with lookup table and FK column
- [ ] The migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Run the migration up against a test database and verify the enum type, column, and backfilled data
- [ ] Run the migration down and verify the lookup table and FK column are restored
- [ ] Verify that no data is lost during the up/down cycle

## Verification Commands
- `cargo test -p migration` — verify migration compiles and passes existing migration tests
- `sea-orm-cli migrate up` — apply migration to dev database
- `sea-orm-cli migrate down` — verify reversibility

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
