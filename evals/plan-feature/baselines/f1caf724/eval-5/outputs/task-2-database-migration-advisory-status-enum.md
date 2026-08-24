## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that converts the advisory status storage from a lookup table to a PostgreSQL enum column. The migration must: (1) create the `advisory_status_enum` type with values New, Analyzing, Fixed, Rejected; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the `status` column from the existing `advisory_status` join; (4) set the `status` column to NOT NULL; (5) drop the `status_id` foreign key column; (6) drop the `advisory_status` lookup table. The down migration must reverse all steps to allow rollback.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — new migration module implementing the enum conversion with up and down functions

## Files to Modify
- `migration/src/lib.rs` — register the new `m0002_advisory_status_enum` migration module
- `migration/Cargo.toml` — add any additional dependencies if needed for enum type support

## Implementation Notes
The migration must be atomic per the feature's non-functional requirements: if any step fails, the entire migration rolls back. Use SeaORM's migration framework with `sea_orm_migration::prelude::*`.

The up migration should execute these SQL statements in order:
1. `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
2. `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`
3. `UPDATE advisory SET status = (SELECT name::advisory_status_enum FROM advisory_status WHERE advisory_status.id = advisory.status_id)`
4. `ALTER TABLE advisory ALTER COLUMN status SET NOT NULL`
5. `ALTER TABLE advisory DROP COLUMN status_id`
6. `DROP TABLE advisory_status`

The down migration must reverse in opposite order:
1. Recreate `advisory_status` table with `id` and `name` columns
2. Insert the four status values (New, Analyzing, Fixed, Rejected)
3. Add `status_id` column back to `advisory` with FK constraint
4. Backfill `status_id` from `status` enum values
5. Drop `status` column
6. `DROP TYPE advisory_status_enum`

Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and SeaORM migration API usage.

Per CONVENTIONS.md §Framework: use SeaORM migration API for all schema changes.
Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's SeaORM database scope.

## Acceptance Criteria
- [ ] Migration `m0002_advisory_status_enum` is registered in `migration/src/lib.rs`
- [ ] Up migration creates `advisory_status_enum` type with four values (New, Analyzing, Fixed, Rejected)
- [ ] Up migration adds `status` column to `advisory` table and backfills from `advisory_status` join
- [ ] Up migration drops `status_id` column and `advisory_status` table
- [ ] Down migration fully reverses the up migration (recreates table, restores FK column, drops enum type)
- [ ] Migration is atomic: partial failure rolls back all changes

## Test Requirements
- [ ] Verify the up migration runs successfully against a test database with existing advisory data
- [ ] Verify the down migration restores the original schema (advisory_status table, status_id FK)
- [ ] Verify that advisory rows retain their correct status values after the backfill
- [ ] Verify the migration handles NULL status_id values gracefully (if any exist)

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without errors
- `cargo run --bin migration -- down` — rollback completes without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
