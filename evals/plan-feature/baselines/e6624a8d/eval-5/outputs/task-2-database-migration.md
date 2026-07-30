## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that performs the full advisory status schema transformation:
1. Define the `advisory_status_enum` PostgreSQL enum type with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `advisory_status` lookup table via the `status_id` foreign key join
4. Drop the `status_id` foreign key column from the `advisory` table
5. Drop the `advisory_status` lookup table

The migration must be atomic (all steps in a single transaction) and reversible (the down migration recreates the lookup table, re-adds the FK column, and backfills from the enum column).

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration module implementing the enum type creation, column addition, backfill, FK drop, and table drop

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration list
- `migration/Cargo.toml` — add any required dependencies if not already present

## Implementation Notes
- Use SeaORM migration framework (`sea_orm_migration::prelude::*`) for the migration definition
- The migration must execute all steps within a single transaction to ensure atomicity — if any step fails, the entire migration rolls back
- For the backfill step, use a SQL statement like: `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum`
- The down migration must reverse in exact opposite order: recreate `advisory_status` table, add `status_id` column, backfill from enum, drop `status` column, drop enum type
- Zero downtime requirement: the migration adds the new column before dropping the old one, allowing a brief window where both exist

Per CONVENTIONS.md §Framework: use SeaORM migration patterns for defining the migration struct and implementing `MigrationTrait`.
Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's SeaORM database framework scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — reference for the established migration structure, table creation patterns, and SeaORM migration trait implementation

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` column of type `advisory_status_enum` to `advisory` table
- [ ] Migration backfills `status` column from existing `advisory_status` join data
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is fully reversible — down migration restores the original schema
- [ ] All steps execute within a single transaction

## Test Requirements
- [ ] Run migration up against a test database and verify enum type exists (`SELECT typname FROM pg_type WHERE typname = 'advisory_status_enum'`)
- [ ] Verify `advisory` table has `status` column and no `status_id` column after migration
- [ ] Verify `advisory_status` table does not exist after migration
- [ ] Run migration down and verify original schema is restored (lookup table exists, FK column exists, enum type dropped)
- [ ] Verify backfill correctness: all advisory rows have a non-null `status` value matching their original `advisory_status` row

## Verification Commands
- `cargo run --bin migration -- up` — run migration and verify success
- `cargo run --bin migration -- down` — run down migration and verify reversibility

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
