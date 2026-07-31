## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create an atomic, reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must perform all steps in a single transaction to ensure atomicity -- if any step fails, the entire migration rolls back, preventing a partial state where the enum column exists but the lookup table is already dropped (or vice versa).

The migration must:
1. Create the `advisory_status_enum` PostgreSQL enum type with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the new `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum`)
4. Set the `status` column to `NOT NULL` after backfill
5. Drop the `status_id` foreign key constraint and column from the `advisory` table
6. Drop the `advisory_status` lookup table

The down migration must reverse all steps: recreate the lookup table, add the FK column, backfill from the enum, and drop the enum type.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- atomic migration implementing all six steps above

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module in the migration runner

## Implementation Notes
- Use SeaORM's migration framework (`sea_orm_migration::prelude::*`) to define the migration
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and conventions
- The migration must be wrapped in a single transaction to satisfy the atomicity NFR. Use `manager.get_connection()` to execute raw SQL within the transaction when SeaORM's schema builder does not support enum operations natively
- For the PostgreSQL enum type creation, use raw SQL: `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
- For the backfill, use a single UPDATE statement joining `advisory` and `advisory_status` to populate the new column
- Ensure the down migration recreates the lookup table with the same four status rows and re-populates `status_id` from the enum column before dropping the enum type
- Zero downtime requirement: the migration adds the new column and backfills before dropping the old one, so queries using either column will work during the migration window

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` column of type `advisory_status_enum` to the `advisory` table
- [ ] Migration backfills the `status` column from the existing `advisory_status` join
- [ ] Migration sets `status` column to NOT NULL after backfill
- [ ] Migration drops the `status_id` FK constraint and column from the `advisory` table
- [ ] Migration drops the `advisory_status` lookup table
- [ ] All steps execute within a single transaction (atomic rollback on failure)
- [ ] Down migration reverses all steps and restores the original schema
- [ ] Migration module is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Run migration up against a test database with existing advisory rows -- verify `status` column is populated correctly
- [ ] Run migration down after up -- verify the original schema (lookup table, FK column) is restored
- [ ] Verify migration fails atomically if any step encounters an error (e.g., simulate a backfill failure)

## Verification Commands
- `cargo run --bin migration -- up` -- migration completes without errors
- `cargo run --bin migration -- down` -- rollback completes without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
