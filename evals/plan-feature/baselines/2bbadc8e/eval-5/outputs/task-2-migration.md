## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create an atomic database migration that converts the advisory status storage from a lookup table (`advisory_status`) to a PostgreSQL enum column on the `advisory` table. The migration must:

1. Create the `advisory_status_enum` PostgreSQL enum type with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `advisory_status` join (`advisory.status_id` -> `advisory_status.id`)
4. Drop the `status_id` foreign key constraint and column from the `advisory` table
5. Drop the `advisory_status` lookup table

All steps must execute within a single transaction so that a failure at any step rolls back the entire migration, preventing an inconsistent state (e.g., enum column exists but lookup table already dropped).

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- migration implementing the enum conversion (up and down)

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module in the migration list
- `migration/Cargo.toml` -- add any required dependencies if needed

## Implementation Notes
- Use SeaORM's migration framework (`sea_orm_migration::prelude::*`) to define the migration
- The `up` method should: (1) create the enum type using raw SQL (`CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`), (2) add the `status` column with a default, (3) backfill from the join (`UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum`), (4) make `status` NOT NULL, (5) drop the `status_id` column, (6) drop the `advisory_status` table
- The `down` method should reverse these operations: recreate the `advisory_status` table, add `status_id` FK column, backfill from enum, drop the `status` column, drop the enum type
- Wrap the backfill and drop in a single transaction to satisfy the atomicity NFR
- Per CONVENTIONS.md §Framework: use SeaORM migration patterns for all DDL operations.
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's SeaORM database scope.
- Reference existing migration pattern in `migration/src/m0001_initial/mod.rs` for the established migration structure

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` -- existing migration demonstrating the project's SeaORM migration pattern (table creation, column definitions)

## Acceptance Criteria
- [ ] Migration `m0002_advisory_status_enum` creates the `advisory_status_enum` PostgreSQL enum type with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] Migration adds a `status` column of type `advisory_status_enum` to the `advisory` table
- [ ] Migration backfills the `status` column from the existing `advisory_status` join
- [ ] Migration drops the `status_id` foreign key column from the `advisory` table
- [ ] Migration drops the `advisory_status` lookup table
- [ ] Migration is fully reversible (down method restores the lookup table and FK column)
- [ ] Migration executes atomically -- if any step fails, all changes are rolled back

## Test Requirements
- [ ] Migration runs successfully against a test database with existing advisory records that have status_id references
- [ ] After migration, advisory records have correct `status` enum values matching their previous `advisory_status` lookup values
- [ ] Migration rollback (down) successfully restores the `advisory_status` table, `status_id` column, and data
- [ ] Migration fails cleanly (full rollback) when the advisory_status table contains an unexpected status value not in the enum

## Verification Commands
- `cargo run -p migration -- up` -- migration applies successfully
- `cargo run -p migration -- down` -- migration rolls back successfully

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
