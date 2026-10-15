## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that drops the `status_id` foreign key column from the `advisory` table and drops the `advisory_status` lookup table entirely. This migration can only run after all code references to the lookup table and the `status_id` column have been removed (Tasks 3, 4, 5). The migration must be reversible: the `down()` method must recreate the `advisory_status` table with its original data and restore the `status_id` column with correct foreign key references.

## Files to Create
- `migration/src/m0003_drop_advisory_status/mod.rs` -- Migration to drop `status_id` column and `advisory_status` table

## Files to Modify
- `migration/src/lib.rs` -- Register the new `m0003_drop_advisory_status` migration module

## Implementation Notes
- In `up()`: (1) drop the foreign key constraint on `advisory.status_id`, (2) drop the `status_id` column from the `advisory` table, (3) drop the `advisory_status` table
- In `down()`: (1) recreate the `advisory_status` table with `id` (primary key) and `name` (varchar) columns, (2) insert the four status rows (New, Analyzing, Fixed, Rejected), (3) add `status_id` column to `advisory` table, (4) backfill `status_id` from the `status` enum column using a join, (5) add the foreign key constraint
- Order matters: drop the FK constraint before the column, drop the column before the table
- Per CONVENTIONS.md §Framework: use SeaORM migration traits for the database migration.
  Applies: task creates `migration/src/m0003_drop_advisory_status/mod.rs` matching the convention's Rust file scope.
- See `migration/src/m0001_initial/mod.rs` for the established migration pattern
- See `migration/src/m0002_advisory_status_enum/mod.rs` (Task 2) for the companion migration that creates the enum

## Acceptance Criteria
- [ ] Migration drops the foreign key constraint on `advisory.status_id`
- [ ] Migration drops the `status_id` column from the `advisory` table
- [ ] Migration drops the `advisory_status` table
- [ ] Migration is reversible: `down()` recreates the table, restores the column, and restores the FK
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] Migration runs successfully after Tasks 2, 3, 4, 5 changes are applied

## Test Requirements
- [ ] Run migration against a test database after the enum migration and code changes are applied; verify `advisory_status` table no longer exists and `status_id` column is removed
- [ ] Run `down()` migration and verify the `advisory_status` table is recreated with all four status rows and `status_id` is restored with correct FK references
- [ ] Verify the migration order: this migration must run after `m0002_advisory_status_enum`

## Verification Commands
- `cargo run --bin migration -- up` -- all migrations complete without error
- `cargo run --bin migration -- down` -- rollback of this migration restores the lookup table

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service and endpoints to use enum column
- Depends on: Task 5 -- Update advisory ingestion pipeline
