# Task 2 — Create database migration for advisory status enum conversion

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that converts the advisory status from a lookup table to a PostgreSQL enum column. The migration must perform the following steps atomically:

1. Create the `advisory_status_enum` PostgreSQL enum type with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `advisory_status` lookup table via the `status_id` foreign key join
4. Drop the `status_id` foreign key constraint and column from the `advisory` table
5. Drop the `advisory_status` lookup table

The migration must be reversible: the down migration must recreate the `advisory_status` table, repopulate it, add the `status_id` FK column back, backfill it from the enum column, and drop the enum column and type.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration to convert advisory status from lookup table to enum column

## Files to Modify
- `migration/src/lib.rs` — register the new migration module
- `migration/Cargo.toml` — add any needed dependencies for enum support if not already present

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and SeaORM migration trait implementation
- Use `sea_orm_migration::prelude::*` and implement both `up` and `down` methods on the `Migration` struct
- For the enum type creation, use raw SQL via `manager.get_connection().execute_unprepared()` since SeaORM migrations support raw PostgreSQL DDL
- The backfill step should use a single UPDATE statement joining `advisory` with `advisory_status`: `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum`
- Per the NFR, the entire migration must be atomic — SeaORM migrations run in a transaction by default, which satisfies this requirement
- Per the NFR, the migration must be safe to run while the application is serving traffic — enum type creation and column addition are non-blocking DDL operations in PostgreSQL
- Error handling: use `.context()` wrapping per the project's error handling convention (see `common/src/error.rs`)

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration structure and SeaORM migration trait implementation pattern

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` enum column to `advisory` table
- [ ] Migration backfills `status` column from existing `status_id` join data
- [ ] Migration drops `status_id` FK column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Down migration fully reverses all changes (recreates table, repopulates, restores FK)
- [ ] Migration is atomic — partial failure rolls back all changes

## Test Requirements
- [ ] Run migration up against test database and verify enum type exists with correct values
- [ ] Run migration up and verify all advisory rows have `status` populated correctly from original `status_id` values
- [ ] Run migration up and verify `status_id` column and `advisory_status` table no longer exist
- [ ] Run migration down and verify `advisory_status` table and `status_id` FK column are restored with correct data
- [ ] Run migration against a database with advisory rows in all four statuses to verify complete backfill coverage

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `sea-orm-cli migrate up` — migration applies without error
- `sea-orm-cli migrate down` — migration reverses without error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
