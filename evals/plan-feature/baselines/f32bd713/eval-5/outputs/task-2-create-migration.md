## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that transitions advisory status storage from the `advisory_status` lookup table to a PostgreSQL enum column on the `advisory` table. The migration must be atomic: if any step fails, the entire migration rolls back. The migration performs the following steps in order:

1. Create the `advisory_status_enum` PostgreSQL enum type with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column by joining `advisory.status_id` to `advisory_status.id` and mapping the status name to the corresponding enum value
4. Drop the `status_id` foreign key constraint and column from the `advisory` table
5. Drop the `advisory_status` lookup table

The down migration must reverse these steps: recreate the lookup table, re-add the FK column, backfill from enum, and drop the enum type.

## Files to Create
- `migration/src/m0002_drop_advisory_status/mod.rs` — new migration module implementing the enum conversion

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration runner

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and SeaORM migration API usage.
- Use `sea_orm_migration::prelude::*` and implement the `MigrationTrait` with `up` and `down` methods.
- For the enum type creation, use raw SQL via `manager.get_connection().execute_unprepared()` since SeaORM's migration API does not natively support PostgreSQL enum types.
- The backfill must happen within the same transaction as the column addition to ensure atomicity. Use a single `UPDATE advisory SET status = ... FROM advisory_status WHERE ...` statement.
- Ensure the down migration is fully reversible: recreate `advisory_status` table with id and name columns, re-add `status_id` FK column, backfill from enum column, then drop the enum column and type.
- Per repo Key Conventions §Framework: use SeaORM migration framework consistently.
  Applies: task creates `migration/src/m0002_drop_advisory_status/mod.rs` matching the convention's migration file scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration demonstrating the SeaORM migration pattern, table creation, and index creation conventions

## Acceptance Criteria
- [ ] Migration `m0002_drop_advisory_status` is registered in `migration/src/lib.rs`
- [ ] Running the migration creates `advisory_status_enum` type with values (New, Analyzing, Fixed, Rejected)
- [ ] Running the migration adds `status` enum column to `advisory` table
- [ ] Running the migration backfills `status` from the existing `status_id` join
- [ ] Running the migration drops `status_id` FK column from `advisory` table
- [ ] Running the migration drops `advisory_status` table
- [ ] Down migration reverses all changes and restores the lookup table with original data
- [ ] Migration is safe to run while the application is serving traffic (zero downtime)

## Test Requirements
- [ ] Migration up succeeds against a database with existing advisory data
- [ ] Migration down succeeds and restores the original schema
- [ ] Backfill correctly maps all four status values (New, Analyzing, Fixed, Rejected)
- [ ] Migration fails atomically if any step encounters an error (no partial state)

## Verification Commands
- `cargo run -p migration -- up` — migration completes without error
- `cargo run -p migration -- down` — rollback completes without error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
