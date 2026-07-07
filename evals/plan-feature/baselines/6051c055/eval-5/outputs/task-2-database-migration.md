# Task 2 — Create database migration for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be atomic: if any step fails, the entire migration rolls back. The migration performs the following steps in order:

1. Create the `advisory_status_enum` PostgreSQL enum type with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = advisory_status.name FROM advisory_status WHERE advisory.status_id = advisory_status.id`)
4. Set the `status` column to NOT NULL after backfill
5. Drop the `status_id` foreign key constraint and column from the `advisory` table
6. Drop the `advisory_status` lookup table

The down migration must reverse these steps: recreate the lookup table, re-add the foreign key column, backfill from the enum, and drop the enum type.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — Migration module implementing up/down migration logic

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migrator
- `migration/Cargo.toml` — Add any required dependencies for enum type handling

## Implementation Notes
- Use SeaORM's migration framework (`sea_orm_migration::prelude::*`) to define the migration
- The enum type must be created using raw SQL via `manager.get_connection().execute_unprepared()` since SeaORM does not have native enum type creation support
- Wrap the backfill and column operations in a single transaction to ensure atomicity
- The migration must be safe to run while the application is serving traffic (zero downtime requirement) — use `ADD COLUMN ... DEFAULT NULL` first, then backfill, then set NOT NULL, to avoid locking the table during the backfill
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and naming conventions
- Per CONVENTIONS.md §Framework: use SeaORM migration patterns consistent with the project's database framework.
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's Rust migration file scope.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` type with four values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` enum column to `advisory` table
- [ ] Migration backfills `status` from the `advisory_status` join
- [ ] Migration drops `status_id` column and foreign key constraint
- [ ] Migration drops `advisory_status` table
- [ ] Down migration reverses all changes (recreates table, re-adds FK, drops enum)
- [ ] Migration is atomic — partial failure rolls back all changes

## Test Requirements
- [ ] Run migration up against a test database with existing advisory data and verify enum column is populated correctly
- [ ] Run migration down and verify the lookup table and FK column are restored
- [ ] Verify that the migration is idempotent (running up twice does not error)
- [ ] Verify that the backfill correctly maps all existing status values

## Verification Commands
- `cargo run -p migration -- up` — migration completes without errors
- `cargo run -p migration -- down` — rollback completes without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
