## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that introduces the `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), adds a `status` enum column to the `advisory` table, and backfills it from the existing `status_id` foreign key join against the `advisory_status` lookup table. The backfill must occur within the same migration to ensure atomicity -- if any step fails, the entire migration rolls back. This migration must be safe to run while the application is serving traffic (zero downtime).

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- Migration to create the `advisory_status_enum` type, add `status` column to `advisory`, and backfill values from `advisory_status` join

## Files to Modify
- `migration/src/lib.rs` -- Register the new `m0002_advisory_status_enum` migration module

## Implementation Notes
- Use SeaORM's `MigrationTrait` to implement `up()` and `down()` methods
- In `up()`: (1) create the enum type using raw SQL `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`, (2) add the `status` column as `advisory_status_enum` with a default, (3) backfill using `UPDATE advisory SET status = s.name::advisory_status_enum FROM advisory_status s WHERE advisory.status_id = s.id`, (4) set the column to NOT NULL after backfill
- In `down()`: (1) drop the `status` column, (2) drop the `advisory_status_enum` type
- The migration must be a single transaction to ensure atomicity -- if backfill fails, the enum type creation is also rolled back
- Zero downtime requirement: the `status` column is added alongside `status_id` (not replacing it yet), so existing queries continue to work during migration
- Per CONVENTIONS.md §Framework: use SeaORM migration traits for the database migration.
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's Rust file scope.
- See `migration/src/m0001_initial/mod.rs` for the established migration pattern in this repository

## Acceptance Criteria
- [ ] Migration `m0002_advisory_status_enum` creates the `advisory_status_enum` PostgreSQL enum type with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] Migration adds a `status` column of type `advisory_status_enum` to the `advisory` table
- [ ] Migration backfills the `status` column from the existing `advisory_status` lookup table join
- [ ] Migration is reversible: `down()` drops the `status` column and the enum type
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] Migration runs successfully against a database with existing advisory data

## Test Requirements
- [ ] Run migration against a test database with seed data containing all four status values and verify each row's `status` column matches the original `advisory_status` row
- [ ] Run `down()` migration and verify the `status` column and enum type are removed
- [ ] Verify migration is atomic: simulate a failure mid-backfill and confirm no partial state remains

## Verification Commands
- `cargo run --bin migration -- up` -- migration completes without error
- `cargo run --bin migration -- down` -- rollback completes without error

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
