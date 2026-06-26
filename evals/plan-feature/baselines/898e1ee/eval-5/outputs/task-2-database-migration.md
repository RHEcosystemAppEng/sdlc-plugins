## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: create the `advisory_status_enum` type with values (New, Analyzing, Fixed, Rejected), add a `status` enum column to the `advisory` table, backfill it from the existing `status_id` join, drop the `status_id` foreign key column, and drop the `advisory_status` table. All steps must be atomic within a single migration so a failure at any point rolls back cleanly.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- migration module: create enum type, add column, backfill, drop FK column, drop lookup table (with reversible down function)

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module m0002_advisory_status_enum in the Migrator vec

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure (MigrationTrait with up/down functions).
- The `up` function should execute these steps in order within a single migration:
  1. `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
  2. `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`
  3. `UPDATE advisory SET status = s.name::advisory_status_enum FROM advisory_status s WHERE advisory.status_id = s.id` (backfill)
  4. `ALTER TABLE advisory ALTER COLUMN status SET NOT NULL` (after backfill)
  5. `ALTER TABLE advisory DROP COLUMN status_id` (drops the FK constraint implicitly)
  6. `DROP TABLE advisory_status`
- The `down` function must reverse all steps: recreate the lookup table, add `status_id` column, backfill from enum, drop the `status` column, drop the enum type.
- Register the new migration in `migration/src/lib.rs` by adding it to the vec returned by `Migrator::migrations()`.
- Per CONVENTIONS.md §Migration Patterns (inferred from repo structure): follow the `m000N_<name>/mod.rs` naming pattern for the migration directory and module. Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's migration file scope.

## Acceptance Criteria
- [ ] Migration `m0002_advisory_status_enum` exists and is registered in `migration/src/lib.rs`
- [ ] Running the migration up creates the `advisory_status_enum` type and `status` column on `advisory`
- [ ] Existing rows are backfilled from the `advisory_status` join
- [ ] The `status_id` column and `advisory_status` table are dropped after backfill
- [ ] Running the migration down fully reverses all changes (table, FK column, and enum type restored)
- [ ] Migration is atomic: partial failure rolls back cleanly

## Test Requirements
- [ ] Migration up succeeds on a database with existing advisory rows that have various status_id values
- [ ] Migration down succeeds and restores the original schema with data intact
- [ ] Verify that after migration up, `advisory.status` contains correct enum values matching original `advisory_status` rows

## Verification Commands
- `cargo run -p migration -- up` -- migration completes without error
- `cargo run -p migration -- down` -- rollback completes without error

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:19f8fd27177ce5d67361cec2aadb8b006ca375c1a9654a6ef1ece0e1223920b3
