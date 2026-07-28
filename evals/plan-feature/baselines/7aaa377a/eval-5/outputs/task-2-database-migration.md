## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create an atomic database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must perform all steps in a single transaction to ensure atomicity: create the `advisory_status_enum` type, add the `status` enum column, backfill existing rows from the `status_id` join, drop the `status_id` foreign key column, and drop the `advisory_status` table. If any step fails, the entire migration must roll back — a partial migration would leave the database in an inconsistent state.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — atomic migration: create enum type, add column, backfill, drop FK, drop table

## Files to Modify
- `migration/src/lib.rs` — register the new migration module
- `migration/Cargo.toml` — add migration module if needed

## Implementation Notes
- The migration must be reversible per the feature requirements. The `down()` method should recreate the `advisory_status` table, add `status_id` FK column, backfill from enum values, and drop the enum column and type.
- Use SeaORM migration framework (`MigrationTrait` implementation) following the pattern in `migration/src/m0001_initial/mod.rs`.
- The enum type values are: `New`, `Analyzing`, `Fixed`, `Rejected` — these are the four stable statuses that have been unchanged for over a year.
- Backfill strategy: `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum` — adjust casting based on the actual lookup table column names.
- Zero downtime requirement: the migration must be safe to run while the application is serving traffic. Adding a column with a default and backfilling in-transaction is safe for PostgreSQL.
- Per CONVENTIONS.md §Framework: use SeaORM migration patterns for all schema changes.
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's Rust/SeaORM migration file scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration demonstrating the project's SeaORM migration pattern (MigrationTrait implementation, up/down methods)

## Acceptance Criteria
- [ ] PostgreSQL enum type `advisory_status_enum` is created with values (New, Analyzing, Fixed, Rejected)
- [ ] `advisory` table has a `status` column of type `advisory_status_enum`
- [ ] All existing rows are backfilled with the correct enum value from the former `status_id` join
- [ ] `status_id` foreign key column is dropped from the `advisory` table
- [ ] `advisory_status` lookup table is dropped
- [ ] Migration is atomic — all steps succeed or all roll back
- [ ] Migration is reversible (down migration restores the lookup table)

## Test Requirements
- [ ] Run the migration against a test database and verify the enum type exists
- [ ] Verify existing advisory rows have correct `status` values after backfill
- [ ] Run the down migration and verify the lookup table is restored with correct data
- [ ] Verify migration is safe to run while the application serves traffic (no exclusive locks on advisory table)

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without error
- `psql -c "SELECT enum_range(NULL::advisory_status_enum)"` — returns {New,Analyzing,Fixed,Rejected}
- `psql -c "SELECT count(*) FROM advisory WHERE status IS NULL"` — returns 0 (all rows backfilled)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
