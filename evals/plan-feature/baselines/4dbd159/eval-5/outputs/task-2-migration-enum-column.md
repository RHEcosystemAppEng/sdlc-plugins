# Task 2 — Create atomic migration to replace advisory_status table with enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a single, atomic database migration that:
1. Creates the `advisory_status_enum` PostgreSQL enum type with values `New`, `Analyzing`, `Fixed`, `Rejected`
2. Adds a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfills the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = advisory_status.name FROM advisory_status WHERE advisory.status_id = advisory_status.id`)
4. Sets `status` column to `NOT NULL` after backfill
5. Drops the `status_id` foreign key constraint and column from the `advisory` table
6. Drops the `advisory_status` table

The migration must be reversible: the down migration must recreate the `advisory_status` table, re-add the `status_id` column, backfill from the enum column, and drop the enum type. If any step fails, the entire migration must roll back atomically.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — the migration module implementing the enum type creation, column addition, backfill, FK drop, and table drop

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration runner

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for structure and conventions
- Use SeaORM's migration API (`sea_orm_migration::prelude::*`) for schema changes
- The migration must be atomic: wrap all steps in a single `up()` method. PostgreSQL DDL is transactional, so if any statement fails the entire migration rolls back
- Use raw SQL via `manager.get_connection().execute_unprepared()` for:
  - `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
  - The backfill UPDATE statement
  - `DROP TYPE advisory_status_enum` in the down migration
- For the `down()` migration, reverse the steps: recreate the `advisory_status` table, add `status_id` column, backfill from enum, drop `status` column, drop enum type
- Zero-downtime consideration: since the migration and code changes land together on the feature branch, the migration runs before the new code is deployed. During the brief window between migration and deployment, the old code still expects the join — but since this is a feature branch, there is no production traffic on it. On merge to main, the migration and code ship together.

## Acceptance Criteria
- [ ] Migration `up()` creates the `advisory_status_enum` type with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] Migration `up()` adds `status` column of type `advisory_status_enum` to `advisory` table
- [ ] Migration `up()` backfills the `status` column from the `advisory_status` join
- [ ] Migration `up()` drops the `status_id` column and its foreign key constraint
- [ ] Migration `up()` drops the `advisory_status` table
- [ ] Migration `down()` reverses all changes: recreates table, re-adds FK column, backfills, drops enum column and type
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] Running the migration against a test database with existing advisory data succeeds without errors

## Test Requirements
- [ ] Run the migration up against a PostgreSQL test database with seeded advisory data and verify the `status` column is correctly populated
- [ ] Run the migration down and verify the `advisory_status` table and `status_id` column are restored with correct data
- [ ] Verify that the `advisory_status_enum` type exists after up and is removed after down

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without errors
- `cargo run --bin migration -- down` — migration rolls back without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
