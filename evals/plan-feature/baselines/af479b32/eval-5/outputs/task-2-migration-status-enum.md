# Task 2: Create database migration for advisory status enum conversion

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a new SeaORM migration that atomically converts the advisory status storage from a lookup table (`advisory_status`) to a PostgreSQL enum column on the `advisory` table. The migration must execute all steps within a single transaction: create the enum type, add the column, backfill data, drop the foreign key, and drop the lookup table. If any step fails, the entire migration rolls back -- a partial migration would leave the database in an inconsistent state. The migration must also be safe to run while the application is serving traffic (zero downtime).

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- new migration module implementing the atomic enum conversion

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module in the migrator's migration list
- `migration/Cargo.toml` -- add any required dependencies if not already present

## Implementation Notes
- The migration must run all steps in a single transaction to satisfy the atomicity requirement. Use SeaORM's migration `manager` within a single `up` function:
  1. Create the PostgreSQL enum type: `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
  2. Add the `status` column: `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`
  3. Backfill the column: `UPDATE advisory SET status = (SELECT label FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum`
  4. Set the column to NOT NULL after backfill: `ALTER TABLE advisory ALTER COLUMN status SET NOT NULL`
  5. Drop the foreign key constraint on `status_id`
  6. Drop the `status_id` column: `ALTER TABLE advisory DROP COLUMN status_id`
  7. Drop the lookup table: `DROP TABLE advisory_status`
- The `down` function must reverse all steps: recreate the `advisory_status` table, add `status_id` column, backfill from enum, drop `status` column, drop the enum type
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure, imports, and the `MigrationTrait` implementation
- Per CONVENTIONS.md: use SeaORM for database operations.
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's SeaORM database scope.
- For zero-downtime safety: the backfill UPDATE should be batched if the advisory table is large, but since the migration is transactional, the entire operation is atomic. Document this trade-off in a code comment.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` -- existing migration module demonstrating the project's SeaORM migration structure, `MigrationTrait` implementation pattern, and table/column creation conventions

## Acceptance Criteria
- [ ] PostgreSQL enum type `advisory_status_enum` exists with values: New, Analyzing, Fixed, Rejected
- [ ] `advisory` table has a `status` column of type `advisory_status_enum` with NOT NULL constraint
- [ ] `status` column is populated correctly from existing `advisory_status` data for all rows
- [ ] `advisory.status_id` foreign key column is dropped
- [ ] `advisory_status` lookup table is dropped
- [ ] Migration is reversible -- running `down` recreates the lookup table and FK
- [ ] Migration runs atomically in a single transaction (partial failure rolls back all changes)
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Run the migration `up` against an empty database with seeded advisory data and verify the enum column is populated correctly
- [ ] Run the migration `down` and verify the lookup table and FK are restored
- [ ] Verify the migration rolls back cleanly if an intermediate step fails (e.g., simulate a constraint violation)
- [ ] Verify no data loss: the count of advisories before and after migration matches, and status values are preserved

## Verification Commands
- `cargo run --bin migration -- up` -- migration completes without error
- `cargo run --bin migration -- down` -- down migration restores previous schema
- `psql -c "SELECT enumlabel FROM pg_enum WHERE enumtypid = 'advisory_status_enum'::regtype ORDER BY enumsortorder"` -- lists enum values (New, Analyzing, Fixed, Rejected)
- `psql -c "SELECT COUNT(*) FROM advisory WHERE status IS NULL"` -- returns 0 (all rows backfilled)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
