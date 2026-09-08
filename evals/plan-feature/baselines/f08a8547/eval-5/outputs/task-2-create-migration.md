## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration performs the following steps atomically within a single transaction:

1. Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected)
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `advisory_status` lookup table via the `status_id` foreign key join
4. Drop the `status_id` foreign key column from the `advisory` table
5. Drop the `advisory_status` lookup table

The migration must be atomic -- if any step fails, the entire migration rolls back. The migration must also be safe to run while the application is serving traffic (zero downtime).

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module in the migration list

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- migration implementation with `up` and `down` functions

## Implementation Notes
- Use SeaORM's migration framework (`sea_orm_migration::prelude::*`) following the pattern established in `migration/src/m0001_initial/mod.rs`
- The `up` function must execute all five steps within a single transaction to ensure atomicity
- The `down` function must reverse the migration completely: recreate the `advisory_status` lookup table, recreate the `status_id` FK column on `advisory`, backfill `status_id` from enum values, drop the `status` enum column, and drop the `advisory_status_enum` type
- Use raw SQL via `manager.get_connection().execute_unprepared()` for PostgreSQL enum type creation and deletion, since SeaORM does not have native enum DDL support
- Use `INSERT INTO ... SELECT` for the backfill step to populate `status` from the `advisory_status` table via the `status_id` join, within the same transaction
- Per CONVENTIONS.md §Framework: use SeaORM migration patterns for all schema changes.
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's Rust migration file scope.
- Constraint §2.1: commit must reference TC-9005 in the footer
- Constraint §5.1: changes scoped to files listed in this task

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` -- reference for SeaORM migration structure (up/down pattern, table and column creation macros)

## Acceptance Criteria
- [ ] Migration `up` function creates enum type, adds column, backfills data, drops FK column, and drops lookup table in a single transaction
- [ ] Migration `down` function reverses all changes completely and restores the original schema
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] `cargo build -p migration` succeeds
- [ ] The four enum values match exactly: New, Analyzing, Fixed, Rejected

## Test Requirements
- [ ] Verify migration runs successfully against a test PostgreSQL database
- [ ] Verify rollback (`down`) restores the original schema with `advisory_status` lookup table and `status_id` FK column
- [ ] Verify backfill correctly maps all existing `status_id` values to corresponding enum values
- [ ] Verify migration fails atomically if any step encounters an error (no partial state)

## Verification Commands
- `cargo build -p migration` -- compilation succeeds
- `cargo test -p migration` -- migration tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
