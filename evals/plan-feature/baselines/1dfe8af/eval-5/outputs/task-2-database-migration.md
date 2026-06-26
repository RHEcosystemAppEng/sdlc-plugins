# Task 2 — Create atomic migration: enum type, backfill, and table drop

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a single atomic database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: (1) create the `advisory_status_enum` type with values New, Analyzing, Fixed, Rejected; (2) add a `status` column of that enum type to the `advisory` table; (3) backfill the `status` column from the existing `advisory_status` join; (4) make the `status` column NOT NULL; (5) drop the `status_id` foreign key column; and (6) drop the `advisory_status` table. All steps must execute within a single transaction so a failure at any point rolls back completely.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migrator's migration list

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — atomic migration implementing all six steps (create enum, add column, backfill, set NOT NULL, drop FK column, drop lookup table) with a corresponding down migration that reverses the process

## Implementation Notes
Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs`. The new migration module should implement `MigrationTrait` with `up` and `down` methods. Use raw SQL within the SeaORM migration framework for the enum type creation (`CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`). The backfill step should use an `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)` pattern. The down migration should reverse all steps: recreate the lookup table, add `status_id` column back, backfill from enum, drop the enum column, and drop the enum type.

Per CONVENTIONS.md §Migration Patterns (if applicable): ensure indexes are created for any new columns used in WHERE clauses.
Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's migration file scope.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` type with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` column to `advisory` table with type `advisory_status_enum`
- [ ] Migration backfills `status` column from `advisory_status` lookup table join
- [ ] Migration sets `status` column to NOT NULL after backfill
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` table
- [ ] All steps execute in a single transaction (atomic rollback on failure)
- [ ] Down migration reverses all changes cleanly

## Test Requirements
- [ ] Run migration up against a test database with existing advisory rows and verify `status` column is populated correctly
- [ ] Run migration down and verify the `advisory_status` table and `status_id` column are restored
- [ ] Verify migration fails atomically if any step encounters an error (no partial state)

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without errors
- `cargo run --bin migration -- down` — rollback completes without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:b4d7a2f19c3e5801d6f8b2c49e0a3d71f5b8c6e23a7d9041f2c8e5b6a1d3f9e7
