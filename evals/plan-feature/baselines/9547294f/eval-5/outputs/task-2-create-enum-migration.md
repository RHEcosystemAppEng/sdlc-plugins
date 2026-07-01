# Task 2 — Create migration to add advisory_status_enum and migrate status column

**Priority:** High
**Fix Versions:** RHTPA 2.0.0
**Labels:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a new SeaORM migration that performs the full status column migration atomically: creates the `advisory_status_enum` PostgreSQL enum type, adds a `status` enum column to the `advisory` table, backfills it from the existing `status_id` join, drops the `status_id` foreign key column, and drops the `advisory_status` lookup table. All steps must execute within a single transaction so that a failure at any point rolls back the entire migration.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration list

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration implementing the enum type creation, column addition, backfill, FK column drop, and table drop

## Implementation Notes
- The migration must be wrapped in a single transaction to satisfy the atomicity requirement (NFR: if any step fails, the entire migration rolls back)
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for the module structure and `MigrationTrait` implementation
- Migration steps in order:
  1. `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
  2. `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`
  3. `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum`
  4. `ALTER TABLE advisory ALTER COLUMN status SET NOT NULL`
  5. `ALTER TABLE advisory DROP COLUMN status_id`
  6. `DROP TABLE advisory_status`
- The down migration should reverse these steps: recreate `advisory_status` table, add `status_id` column, backfill from enum, drop enum column, drop enum type
- Per CONVENTIONS.md Key Conventions: use SeaORM migration patterns (Framework convention).
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's migration file scope.
- Zero downtime consideration: the backfill UPDATE should be safe for concurrent reads since it only writes to the new column while the old column still exists during the transaction

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` enum column to `advisory` table
- [ ] Migration backfills `status` from existing `status_id` join data
- [ ] Migration drops `status_id` foreign key column
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is atomic — all steps in a single transaction
- [ ] Down migration reverses all changes cleanly

## Test Requirements
- [ ] Run migration up against a test database with existing advisory data and verify `status` column is populated correctly
- [ ] Run migration down and verify the original schema is restored with data intact
- [ ] Verify migration handles empty `advisory` table (no rows to backfill) without error

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without error
- `cargo run --bin migration -- down` — rollback completes without error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3
