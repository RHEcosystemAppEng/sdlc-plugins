# Task 2 — Create migration to replace advisory_status table with enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be atomic: if any step fails, the entire migration rolls back. The migration must be safe to run while the application is serving traffic (zero downtime).

The migration performs these steps in order:
1. Create the `advisory_status_enum` PostgreSQL enum type with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = advisory_status.name FROM advisory_status WHERE advisory.status_id = advisory_status.id`)
4. Set the `status` column to NOT NULL after backfill
5. Drop the `status_id` foreign key constraint from the `advisory` table
6. Drop the `status_id` column from the `advisory` table
7. Drop the `advisory_status` table

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration module implementing the enum column migration

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration runner

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and registration
- The migration must implement both `up()` and `down()` methods for reversibility
- The `down()` method must: recreate `advisory_status` table, repopulate it, add `status_id` column, backfill `status_id` from `status`, drop `status` column, drop `advisory_status_enum` type
- Use SeaORM migration API (`sea_orm_migration::prelude::*`) for all DDL operations
- Wrap all operations in a single transaction to ensure atomicity — a partial migration (enum column exists but lookup table already dropped, or vice versa) would leave the database inconsistent
- For zero-downtime safety: the backfill uses UPDATE...FROM which acquires row-level locks, not table-level locks. Avoid `ALTER TABLE ... RENAME` on hot tables; instead add the new column, backfill, then drop the old column
- The enum type should be created using raw SQL via `manager.get_connection().execute_unprepared()` since SeaORM does not have native PostgreSQL enum DDL support

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern showing the module structure, `MigrationTrait` implementation, and table/column definition approach

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` type with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` column to `advisory` table using the enum type
- [ ] Migration backfills `status` from the existing `status_id` join
- [ ] Migration drops `status_id` column and `advisory_status` table
- [ ] Migration is fully reversible (down migration recreates the lookup table and restores `status_id`)
- [ ] Migration is atomic — all steps succeed or all roll back

## Test Requirements
- [ ] Migration applies successfully on a fresh database (up)
- [ ] Migration rolls back successfully (down) and restores the original schema
- [ ] Migration handles existing data correctly during backfill (all four status values)
- [ ] Migration is safe to run on a non-empty `advisory` table

## Verification Commands
- `cargo run -p migration -- up` — migration applies without error
- `cargo run -p migration -- down` — migration rolls back without error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
