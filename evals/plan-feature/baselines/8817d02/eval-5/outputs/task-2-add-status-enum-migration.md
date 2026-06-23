# Task 2 — Add database migration for advisory status enum column

## Summary

Create reversible migration to add advisory_status_enum type and status column to advisory table

## Repository

trustify-backend

## Target Branch

TC-9005

## Description

Create a new SeaORM migration that:
1. Creates the PostgreSQL enum type `advisory_status_enum` with values (`New`, `Analyzing`, `Fixed`, `Rejected`).
2. Adds a `status` column of type `advisory_status_enum` to the `advisory` table.
3. Backfills the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = advisory_status.value FROM advisory_status WHERE advisory.status_id = advisory_status.id`).
4. Sets the `status` column to NOT NULL after backfill.
5. Drops the `status_id` foreign key column from the `advisory` table.
6. Drops the `advisory_status` lookup table.

The migration must be reversible: the down migration re-creates the lookup table, re-adds the FK column, backfills from the enum column, and drops the enum type.

## Files to Create

- `migration/src/m0002_advisory_status_enum/mod.rs` — new migration module implementing the enum type creation, column addition, backfill, FK drop, and table drop

## Files to Modify

- `migration/src/lib.rs` — register the new migration module in the migration list

## Implementation Notes

- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and conventions.
- Use SeaORM's `manager.create_type()` for the PostgreSQL enum creation and `manager.drop_type()` in the down migration.
- The migration must be atomic — wrap all steps in a single transaction so if any step fails, the entire migration rolls back. This is a non-functional requirement of the feature.
- The migration must be safe to run while the application is serving traffic (zero downtime requirement). The backfill should use batched updates if the advisory table is large.
- Ensure the down migration re-creates the `advisory_status` table with the same schema as the original, re-adds `status_id` FK column, backfills from the enum column, and drops the enum type.

## Reuse Candidates

- `migration/src/m0001_initial/mod.rs` — reference for migration structure, transaction wrapping, and SeaORM migration API usage

## Acceptance Criteria

- [ ] Running the migration creates the `advisory_status_enum` type in PostgreSQL
- [ ] The `advisory` table has a `status` column of type `advisory_status_enum`
- [ ] All existing rows in `advisory` have their `status` column populated from the old `status_id` join
- [ ] The `status_id` column no longer exists on the `advisory` table
- [ ] The `advisory_status` table no longer exists
- [ ] Running the down migration reverses all changes and restores the original schema
- [ ] The migration is atomic — partial failures leave the database unchanged

## Test Requirements

- [ ] Verify the up migration succeeds on a database with existing advisory data
- [ ] Verify the down migration restores the original schema and data
- [ ] Verify that the migration is idempotent when re-run after rollback
- [ ] Verify that the `status` column values match the original `advisory_status` lookup values after backfill

## Verification Commands

- `cargo run --bin migration -- up` — migration completes without errors
- `cargo run --bin migration -- down` — rollback completes without errors
- `psql -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'advisory' AND column_name = 'status'"` — confirms enum column exists

## Dependencies

- Depends on: Task 1 — Create feature branch TC-9005 from main

sha256-md:cca385e755ba83359147014ec872c6dba9017a590329141e483023652af11869
