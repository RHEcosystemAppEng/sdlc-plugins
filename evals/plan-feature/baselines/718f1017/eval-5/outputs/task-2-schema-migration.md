# Task 2 — Create database migration for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a new SeaORM database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be atomic and reversible: if any step fails, the entire migration rolls back. This is the foundational change that all other tasks in this feature depend on.

The migration must perform the following steps in order:
1. Create the `advisory_status_enum` PostgreSQL enum type with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `status_id` FK join to `advisory_status`
4. Drop the `status_id` foreign key constraint and column from the `advisory` table
5. Drop the `advisory_status` lookup table

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — new migration module implementing the enum migration

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration runner

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for module structure and registration
- Use SeaORM's `extension::postgres::Type` for creating the PostgreSQL enum type
- The backfill step should use a single `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE id = advisory.status_id)` or equivalent SeaORM expression
- The `down()` migration must reverse all steps: recreate the `advisory_status` table, add `status_id` back, backfill from enum, and drop the enum type
- Per the feature's non-functional requirements: migration must be safe to run while the application is serving traffic (zero downtime). Consider using `ALTER TABLE ... ADD COLUMN ... DEFAULT` which is non-blocking in PostgreSQL 11+
- Per docs/constraints.md section 2 (Commit Rules): commit must reference TC-9005 in the footer and follow Conventional Commits format
- Per docs/constraints.md section 5 (Code Change Rules): inspect existing migration code before implementing

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` type with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` column to `advisory` table using the enum type
- [ ] Migration backfills `status` from the `status_id` join in the same transaction
- [ ] Migration drops `status_id` FK column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is reversible — `down()` restores the previous schema
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration `up()` completes successfully against a test database with existing advisory data
- [ ] Migration `down()` restores the original schema (advisory_status table, status_id FK column)
- [ ] Backfill correctly maps all four status values
- [ ] Migration handles the case where `advisory` table has no rows (empty backfill)

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `sea-orm-cli migrate up` — migration applies cleanly

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:5bcecf4daedddacc99a7f08ff66a376784e001dfa7d6bac7499f5e44a14c2b4a
