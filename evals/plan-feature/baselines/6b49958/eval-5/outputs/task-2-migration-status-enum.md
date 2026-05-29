## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: (1) create the `advisory_status_enum` type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of that enum type to the `advisory` table; (3) backfill the `status` column from the existing `advisory_status` join; (4) drop the `status_id` foreign key column; (5) drop the `advisory_status` table. The down migration must reverse all steps.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration module implementing up/down for the enum conversion

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration list

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and SeaORM migration trait implementation.
- The up migration must execute steps in this exact order: (1) create enum type, (2) add column with default, (3) backfill via UPDATE ... FROM join, (4) remove default and set NOT NULL, (5) drop FK column `status_id`, (6) drop `advisory_status` table.
- The down migration must reverse: (1) recreate `advisory_status` table with the four status rows, (2) add `status_id` column, (3) backfill `status_id` from `status` enum, (4) add FK constraint, (5) drop `status` column, (6) drop enum type.
- Use raw SQL via `manager.get_connection().execute_unprepared()` for the PostgreSQL `CREATE TYPE ... AS ENUM` statement since SeaORM's schema manager does not natively support enum type creation.
- Ensure the migration is atomic (all steps in a single transaction) to prevent partial schema states.
- The `advisory_status` table currently has rows for: `New`, `Analyzing`, `Fixed`, `Rejected` — these must match the enum values exactly.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration module demonstrating the SeaORM migration trait pattern and table/column operations

## Acceptance Criteria
- [ ] Running the up migration creates the `advisory_status_enum` type with four values
- [ ] The `advisory.status` column exists and is populated from the old `status_id` join
- [ ] The `status_id` column and `advisory_status` table are dropped
- [ ] Running the down migration restores the original schema (lookup table, FK column)
- [ ] Migration is reversible without data loss

## Test Requirements
- [ ] Test up migration against a database with existing advisory rows having all four status values
- [ ] Test down migration restores the `advisory_status` table and `status_id` column with correct data
- [ ] Test that the migration rolls back cleanly if any step fails (atomic transaction)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256:50e71e504f7c8ba2106c66c6106bed09d28d9aef06c726f130b9e281ce276f88
