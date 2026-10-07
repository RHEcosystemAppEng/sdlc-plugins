## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that converts the advisory status storage from a lookup table to a PostgreSQL enum column. The migration must:

1. Create the `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = s.name FROM advisory_status s WHERE advisory.status_id = s.id`)
4. Drop the `status_id` foreign key column from the `advisory` table
5. Drop the `advisory_status` lookup table

The migration must be atomic -- if any step fails, the entire migration rolls back. The migration must be safe to run while the application is serving traffic (zero downtime).

## Files to Modify
- `migration/src/lib.rs` -- Register the new migration module in the migration runner

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- Migration implementing enum type creation, column addition, backfill, FK column drop, and table drop

## Implementation Notes
- Use SeaORM's migration API (`MigrationTrait`) to define `up()` and `down()` methods
- The `down()` method must reverse all changes: recreate the `advisory_status` table, add `status_id` FK column, backfill from enum column, drop the enum column, drop the enum type
- Use raw SQL via `manager.get_connection().execute_unprepared()` for creating the PostgreSQL enum type, as SeaORM's schema builder does not natively support enum type creation
- Ensure the backfill step handles NULL values gracefully -- if any advisory has no status, assign a default (e.g., `New`)
- The migration runs inside a transaction by default in SeaORM, ensuring atomicity
- See existing migration `migration/src/m0001_initial/mod.rs` for the established migration pattern in this project

Per CONVENTIONS.md §Framework: use SeaORM migration API for all schema changes.
Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's Rust (.rs) file scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` -- Existing migration demonstrating SeaORM's `MigrationTrait` usage, table creation, and column definition patterns

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` column of type `advisory_status_enum` to `advisory` table
- [ ] Migration backfills `status` column from existing `advisory_status` join data
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is reversible -- `down()` method restores the previous schema completely
- [ ] Migration is safe to run while the application is serving traffic

## Test Requirements
- [ ] Run the migration `up()` against a test database and verify the enum type and column exist
- [ ] Run the migration `down()` and verify the lookup table and FK column are restored
- [ ] Verify backfill correctness: all advisory rows have the correct status value derived from the lookup table
- [ ] Verify NULL handling: advisories without a status are assigned the default value

## Verification Commands
- `cargo test -p migration` -- Verify migration compiles and passes any migration-level tests

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
