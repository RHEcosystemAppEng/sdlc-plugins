# Task 2: Write database migration for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a SeaORM migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: (1) create the `advisory_status_enum` PostgreSQL type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the new column from the existing `advisory.status_id` joined with `advisory_status.id`; (4) drop the `status_id` foreign key column from `advisory`; (5) drop the `advisory_status` table. The migration must be atomic and reversible.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration implementing enum creation, column addition, backfill, FK drop, and table drop

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migrator

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and SeaORM migration trait implementation.
- The migration's `up()` must execute steps in order: create enum type, add column, backfill via UPDATE...FROM join, drop FK constraint, drop `status_id` column, drop `advisory_status` table.
- The migration's `down()` must reverse all steps: recreate `advisory_status` table, add `status_id` column, backfill from enum column, drop `status` column, drop enum type.
- Use raw SQL via `manager.get_connection().execute_unprepared()` for the `CREATE TYPE` and backfill statements, as SeaORM's schema manager does not natively support PostgreSQL enum creation.
- Per CONVENTIONS.md §Framework: use SeaORM migration framework for schema changes. Applies: convention has no file-type restriction (broadly applicable).

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` column of type `advisory_status_enum` to `advisory` table
- [ ] Migration backfills `status` from existing `status_id` join with `advisory_status`
- [ ] Migration drops `status_id` foreign key column from `advisory`
- [ ] Migration drops `advisory_status` table
- [ ] Migration is reversible — `down()` restores the original schema
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration runs successfully against a clean database
- [ ] Migration runs successfully against a database with existing advisory data (backfill produces correct enum values)
- [ ] Migration rollback (`down()`) restores the original schema with lookup table and FK column

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without errors
- `cargo run --bin migration -- down` — rollback completes without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
