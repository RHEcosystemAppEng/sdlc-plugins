# Task 2 — Create migration to add advisory status enum and drop lookup table

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that: (1) creates the PostgreSQL enum type `advisory_status_enum` with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) adds a `status` enum column to the `advisory` table; (3) backfills the new `status` column from the existing `advisory_status` join; (4) drops the `status_id` foreign key column from `advisory`; (5) drops the `advisory_status` lookup table. The migration must be atomic — if any step fails, the entire migration rolls back.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration module implementing the enum type creation, column addition, data backfill, FK column drop, and lookup table drop

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration list

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and conventions
- Use SeaORM migration API: `manager.create_type()` for the PostgreSQL enum, `manager.alter_table()` for column additions/drops, `manager.drop_table()` for the lookup table removal
- The backfill step should use a raw SQL `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)` to populate the enum column before dropping the FK
- Ensure the `down()` method reverses all steps: recreate `advisory_status` table, add `status_id` FK column, backfill from enum, drop `status` column, drop enum type
- The migration must be safe to run while the application is serving traffic (zero downtime requirement)
- Per the repo's module pattern: each migration is a separate module under `migration/src/` registered in `migration/src/lib.rs`

## Acceptance Criteria
- [ ] PostgreSQL enum type `advisory_status_enum` is created with values (New, Analyzing, Fixed, Rejected)
- [ ] `advisory` table has a new `status` column of type `advisory_status_enum`
- [ ] All existing rows are backfilled with the correct status value from the `advisory_status` lookup
- [ ] `status_id` foreign key column is removed from `advisory` table
- [ ] `advisory_status` lookup table is dropped
- [ ] Migration is reversible — `down()` restores the previous schema
- [ ] Migration is atomic — partial failure rolls back all changes

## Test Requirements
- [ ] Run the migration `up()` and verify the enum type exists and all rows are backfilled correctly
- [ ] Run the migration `down()` and verify the original schema is restored with data intact
- [ ] Verify that the migration handles edge cases: NULL status_id values (if any), concurrent read queries during migration

## Verification Commands
- `cargo test -p migration` — migration compiles and tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

---
Description Digest: sha256-md:200659be088b401b623dace42f0f95199fcbaa867d1c8e27c91678ef1a88f138
Priority: High
Fix Versions: RHTPA 2.0.0
