## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a new SeaORM migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: create the `advisory_status_enum` type with values (New, Analyzing, Fixed, Rejected), add a `status` enum column to the `advisory` table, backfill it from the existing `status_id` foreign key join, drop the `status_id` column, and drop the `advisory_status` table. The migration must be fully reversible and safe to run under concurrent traffic (zero downtime).

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration implementing enum type creation, column addition, data backfill, FK column drop, and lookup table drop

## Files to Modify
- `migration/src/lib.rs` — register the new `m0002_advisory_status_enum` migration module
- `migration/Cargo.toml` — add module path if needed for the new migration

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and conventions.
- The migration `up()` method should execute these steps in order:
  1. `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
  2. `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`
  3. `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum`
  4. `ALTER TABLE advisory ALTER COLUMN status SET NOT NULL`
  5. `ALTER TABLE advisory DROP COLUMN status_id`
  6. `DROP TABLE advisory_status`
- The `down()` method must reverse all steps to restore the lookup table and FK column.
- Use raw SQL via `manager.get_connection().execute_unprepared()` for enum type creation since SeaORM migrations don't have native enum type support.
- Per CONVENTIONS.md §Key Conventions: use SeaORM for database operations. Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's Rust migration file scope.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` enum column to `advisory` table and backfills from existing `status_id` join
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is reversible — `down()` restores the lookup table, FK column, and removes the enum type
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration runs successfully against a test database with seeded advisory data
- [ ] Backfilled `status` values match the original `advisory_status.name` values
- [ ] Migration rollback restores the original schema with FK column and lookup table
- [ ] Migration is idempotent — running it twice does not error

## Verification Commands
- `cargo test -p migration` — migration compiles and unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:a6a5b4d7c97c442b8f735e3664a17ec061503127aedc97033fc77bf7b89c9a2c
