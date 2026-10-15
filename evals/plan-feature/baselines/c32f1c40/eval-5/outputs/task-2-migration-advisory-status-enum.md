## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that transitions the advisory status storage from a lookup table to a PostgreSQL enum column. The migration must be atomic: if any step fails, the entire migration rolls back. The migration performs these steps in order:

1. Create the `advisory_status_enum` PostgreSQL enum type with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = advisory_status.name FROM advisory_status WHERE advisory.status_id = advisory_status.id`)
4. Set the `status` column to `NOT NULL` after backfill
5. Drop the `status_id` foreign key constraint from the `advisory` table
6. Drop the `status_id` column from the `advisory` table
7. Drop the `advisory_status` lookup table

The down migration must reverse all steps to restore the original schema.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- reversible migration implementing the enum conversion, backfill, FK drop, column drop, and table drop

## Files to Modify
- `migration/src/lib.rs` -- register the new `m0002_advisory_status_enum` migration module
- `migration/Cargo.toml` -- add any additional dependencies if needed for enum support

## Implementation Notes
- Use SeaORM's migration framework (`MigrationTrait`) with `up` and `down` methods
- The migration must run within a single transaction to ensure atomicity -- use `manager.get_connection()` to execute raw SQL within the migration's transaction context
- For zero-downtime safety: the backfill uses the existing `status_id` join to populate the new `status` column before dropping any old columns or tables
- Reference the existing migration pattern in `migration/src/m0001_initial/mod.rs` for the established migration structure (table creation, column definitions, index patterns)
- Use `sea_orm::DbBackend::Postgres` specific SQL for `CREATE TYPE ... AS ENUM` since SeaORM's schema builder does not natively support PostgreSQL enum type creation
- The down migration must: recreate `advisory_status` table, repopulate it, add `status_id` column, backfill it from the enum column, add FK constraint, then drop the `status` column and enum type
- Per CONVENTIONS.md §Framework: use SeaORM migration patterns for all schema changes.
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's SeaORM database scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` -- reference for migration structure, table creation patterns, and SeaORM migration trait implementation

## Acceptance Criteria
- [ ] Migration `m0002_advisory_status_enum` runs successfully against a PostgreSQL database with existing advisory data
- [ ] The `advisory_status_enum` type exists with values: New, Analyzing, Fixed, Rejected
- [ ] The `advisory.status` column exists and is populated with correct enum values for all existing rows
- [ ] The `advisory.status_id` column no longer exists
- [ ] The `advisory_status` table no longer exists
- [ ] The down migration successfully restores the original schema (lookup table, FK column, data)
- [ ] Migration is atomic: partial failure rolls back all changes

## Test Requirements
- [ ] Run migration up against a test database with seeded advisory data and verify enum column is populated correctly
- [ ] Run migration down and verify the original schema (lookup table, FK, data) is fully restored
- [ ] Test migration against empty database (no advisories) to ensure it handles zero-row backfill
- [ ] Verify migration runs within a single transaction (simulate failure mid-migration and confirm rollback)

## Verification Commands
- `cargo run -p migration -- up` -- migration completes without error
- `cargo run -p migration -- down` -- down migration restores original schema
- `psql -c "SELECT enumlabel FROM pg_enum JOIN pg_type ON pg_enum.enumtypid = pg_type.oid WHERE typname = 'advisory_status_enum';"` -- lists enum values

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
