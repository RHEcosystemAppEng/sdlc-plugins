## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that introduces the `advisory_status_enum` PostgreSQL enum type, adds a `status` enum column to the `advisory` table, backfills it from the existing `advisory_status` lookup table join, drops the `status_id` foreign key column, and drops the `advisory_status` table. The migration must be atomic — if any step fails, the entire migration rolls back. The migration must be safe to run while the application is serving traffic (zero downtime).

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the `Migrator` vec

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — new SeaORM migration implementing the enum type creation, column addition, data backfill, FK column drop, and lookup table drop

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and conventions
- Use SeaORM's migration API (`sea_orm_migration::prelude::*`) to define `up()` and `down()` methods
- In `up()`:
  1. Create the enum type: `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
  2. Add the `status` column to the `advisory` table with type `advisory_status_enum`
  3. Backfill: `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum`
  4. Set `status` column to `NOT NULL` after backfill
  5. Drop the `status_id` column (this removes the FK constraint implicitly)
  6. Drop the `advisory_status` table
- In `down()`:
  1. Recreate the `advisory_status` table with id and name columns
  2. Insert the four status rows (New, Analyzing, Fixed, Rejected)
  3. Add `status_id` column to `advisory` table
  4. Backfill `status_id` from the enum column
  5. Add FK constraint on `status_id`
  6. Drop the `status` enum column
  7. Drop the `advisory_status_enum` type
- For zero-downtime safety: use `ALTER TABLE ... ADD COLUMN` with a default value to avoid full table rewrites on PostgreSQL 11+
- Register the migration in `migration/src/lib.rs` by adding `m0002_advisory_status_enum::Migration` to the `Migrator::migrations()` vec, following the pattern of existing entries

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration demonstrating the SeaORM migration pattern, `up()`/`down()` structure, and table/column creation API usage

## Acceptance Criteria
- [ ] `advisory_status_enum` PostgreSQL type is created with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] `advisory.status` column exists with type `advisory_status_enum` and is NOT NULL
- [ ] All existing rows have `status` populated correctly from the former `advisory_status` join
- [ ] `advisory.status_id` column no longer exists
- [ ] `advisory_status` table no longer exists
- [ ] `down()` migration fully reverses all changes and restores the lookup table with data
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Run migration `up()` against a test database with sample advisory rows referencing all four statuses — verify all rows have correct `status` values
- [ ] Run migration `down()` — verify the `advisory_status` table is restored, `status_id` FK is re-established, and enum type is dropped
- [ ] Verify the migration is idempotent: running `up()` twice does not error (second run is a no-op)

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without error
- `cargo run --bin migration -- down` — rollback completes without error
- `psql -c "SELECT enumlabel FROM pg_enum WHERE enumtypid = 'advisory_status_enum'::regtype ORDER BY enumsortorder"` — returns New, Analyzing, Fixed, Rejected

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
