## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must:

1. Create the `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `advisory_status` join (`advisory.status_id` references `advisory_status.id`)
4. Drop the `status_id` foreign key column from the `advisory` table
5. Drop the `advisory_status` lookup table

The migration must be atomic -- if any step fails, the entire migration rolls back. The migration must be safe to run while the application is serving traffic (zero downtime).

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- migration module implementing the enum type creation, column addition, backfill, FK removal, and table drop

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module in the migrator
- `migration/Cargo.toml` -- add migration module to the crate if needed

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for structure and SeaORM migration API usage
- Use SeaORM's migration API (`sea_orm_migration::prelude::*`) for defining up and down operations
- Wrap all operations in a single transaction to ensure atomicity -- if the backfill or any DDL step fails, the entire migration rolls back
- The backfill step should populate `status` from the join: `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)`
- Use `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')` for the PostgreSQL enum type
- The down migration must reverse all steps in order: recreate `advisory_status` table, add `status_id` FK column back, populate FK from enum values, drop `status` enum column, drop `advisory_status_enum` type
- For zero-downtime safety, the enum column should have a NOT NULL constraint added only after backfill completes

Per CONVENTIONS.md section "Framework": use SeaORM migration API for all database schema changes.
Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's Rust file scope.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` enum column to `advisory` table
- [ ] Migration backfills `status` column from existing `advisory_status` join for all rows
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is fully reversible (down migration restores previous schema exactly)
- [ ] All operations execute within a single transaction (atomic rollback on failure)

## Test Requirements
- [ ] Migration applies successfully on a database with existing advisory data
- [ ] Migration rolls back cleanly (down migration restores lookup table and FK)
- [ ] Backfill correctly maps all existing status_id values to the corresponding enum values
- [ ] Migration handles the case where `advisory` table has no rows (empty backfill)
- [ ] Migration is safe to run concurrently with application traffic (no exclusive locks on advisory table)

## Verification Commands
- `cargo run --bin migration -- up` -- migration applies without error
- `cargo run --bin migration -- down` -- migration rolls back without error

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
