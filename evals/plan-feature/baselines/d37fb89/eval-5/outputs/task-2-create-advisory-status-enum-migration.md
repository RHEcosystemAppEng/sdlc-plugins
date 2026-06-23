## Summary
Create database migration for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a new SeaORM migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: (1) create the `advisory_status_enum` PostgreSQL enum type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the new `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = advisory_status.name FROM advisory_status WHERE advisory.status_id = advisory_status.id`); (4) set the `status` column to NOT NULL after backfill; (5) drop the `status_id` foreign key column from the `advisory` table; (6) drop the `advisory_status` table. The migration must be reversible: the down migration recreates the lookup table, re-adds the foreign key column, and backfills from the enum column.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- new migration module implementing up/down for the advisory status enum conversion

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module in the migrator's migration list

## Implementation Notes
Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`. The migration must execute all steps within a single transaction to ensure atomicity -- if any step fails, the entire migration rolls back. Use SeaORM's `manager.exec_stmt()` for raw SQL statements where the query builder does not support PostgreSQL enum operations. The backfill step must handle the case where the `advisory` table has zero rows (no-op). The down migration must reverse each step in the opposite order.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] Migration adds `status` column of type `advisory_status_enum` to `advisory` table
- [ ] Migration backfills `status` column from existing `advisory_status` join
- [ ] Migration sets `status` column to NOT NULL after backfill
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops the `advisory_status` lookup table
- [ ] Down migration reverses all changes and restores the original schema
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Run migration up against a test database with existing advisory rows and verify the `status` column is populated correctly
- [ ] Run migration down and verify the original schema (lookup table, foreign key) is restored
- [ ] Verify migration handles an empty `advisory` table without errors

## Verification Commands
- `cargo run -p migration -- up` -- migration applies successfully
- `cargo run -p migration -- down` -- migration rolls back successfully

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:90e504167b3906866767bd603740fe63dc6602700a44b0cb428baf576177a8fd
