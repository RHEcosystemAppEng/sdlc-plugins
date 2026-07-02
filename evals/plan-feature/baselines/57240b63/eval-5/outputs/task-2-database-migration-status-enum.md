# Task 2 — Create database migration for advisory status enum conversion

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a SeaORM database migration that converts the advisory status storage from a lookup table (`advisory_status`) to a PostgreSQL enum column on the `advisory` table. The migration must be atomic — all steps (enum creation, column addition, backfill, FK drop, table drop) execute within a single transaction so a failure at any point rolls back completely. This eliminates the `advisory_status` join from all advisory queries and simplifies the schema.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — New migration module implementing the enum conversion

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration list
- `migration/Cargo.toml` — Add any additional dependencies if needed for enum support

## Implementation Notes
- Follow the existing migration structure established in `migration/src/m0001_initial/mod.rs` — implement `MigrationTrait` with `up()` and `down()` methods.
- The `up()` migration must execute these steps in order within a single transaction:
  1. Create the PostgreSQL enum type `advisory_status_enum` with values `'New'`, `'Analyzing'`, `'Fixed'`, `'Rejected'`
  2. Add a `status` column of type `advisory_status_enum` to the `advisory` table (initially nullable)
  3. Backfill the `status` column from the existing `advisory_status` join: `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)`
  4. Set the `status` column to `NOT NULL` after backfill
  5. Drop the `status_id` foreign key constraint from `advisory`
  6. Drop the `status_id` column from `advisory`
  7. Drop the `advisory_status` table
- The `down()` migration must reverse all steps: recreate the lookup table, add `status_id` FK, backfill from enum, drop enum column, drop enum type.
- Use `sea_orm_migration::prelude::*` for migration infrastructure.
- Zero downtime consideration: the migration is safe to run while the application is serving traffic because it uses a transaction — concurrent reads will see either the old schema or the new schema, never a partial state.
- Per CONVENTIONS.md §Framework: use SeaORM migration patterns consistent with the existing codebase.
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's migration file scope.

## Acceptance Criteria
- [ ] Migration `m0002_advisory_status_enum` is registered in `migration/src/lib.rs`
- [ ] Running the migration creates the `advisory_status_enum` PostgreSQL enum type
- [ ] The `advisory.status` column exists with type `advisory_status_enum` and `NOT NULL` constraint after migration
- [ ] All existing advisory rows have their `status` column populated from the former `advisory_status` join
- [ ] The `advisory.status_id` column and its FK constraint are dropped
- [ ] The `advisory_status` table is dropped
- [ ] The migration is fully reversible via `down()`
- [ ] A failure at any step rolls back the entire migration (atomic transaction)

## Test Requirements
- [ ] Run migration `up()` against a test database with seeded advisory data and verify enum column is populated correctly
- [ ] Run migration `down()` after `up()` and verify the original schema is restored (lookup table, FK column, data intact)
- [ ] Verify that a partial failure (e.g., simulated error after backfill) rolls back all changes

## Verification Commands
- `cargo run --bin migration -- up` — expected: migration completes successfully
- `cargo run --bin migration -- down` — expected: rollback completes successfully
- `psql -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='advisory' AND column_name='status'"` — expected: column exists with type `USER-DEFINED`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

---

[sdlc-workflow] Description digest: sha256-md:02a57f237dc9f89d78ad1cb4e0027c94540d3d63ed4154ebaba35f79fcb2f5ee
