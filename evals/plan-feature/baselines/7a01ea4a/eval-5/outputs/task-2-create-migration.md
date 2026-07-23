## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create an atomic, reversible database migration that transitions the advisory status storage from a lookup table to a PostgreSQL enum column. The migration must: (1) create the `advisory_status_enum` PostgreSQL enum type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = s.name FROM advisory_status s WHERE advisory.status_id = s.id`); (4) drop the `status_id` foreign key column from `advisory`; (5) drop the `advisory_status` table. The down migration must reverse all steps to restore the original schema.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- migration module implementing the enum type creation, column addition, backfill, FK drop, and table drop

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module in the migration list

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for the SeaORM migration structure (impl `MigrationTrait` with `up` and `down` methods).
- The migration MUST be atomic: wrap all steps in a single transaction so that if any step fails, the entire migration rolls back. A partial migration (enum column exists but lookup table is already dropped, or vice versa) would leave the database in an inconsistent state.
- For the backfill step, use a raw SQL statement to populate the `status` column from the join: `UPDATE advisory SET status = s.name::advisory_status_enum FROM advisory_status s WHERE advisory.status_id = s.id`.
- The down migration must: (1) recreate the `advisory_status` table with its original schema, (2) repopulate it with the four status values, (3) add back the `status_id` FK column to `advisory`, (4) backfill `status_id` from the enum column, (5) drop the `status` enum column, (6) drop the `advisory_status_enum` type.
- Zero downtime: the migration must be safe to run while the application is serving traffic. The backfill and column operations should use `ALTER TABLE ... ADD COLUMN` with a default, not lock the table for extended periods.
- Per docs/constraints.md section 2 (Commit Rules): commit messages must follow Conventional Commits format, reference TC-9005 in the footer, and include the `--trailer="Assisted-by: Claude Code"`.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` column of type `advisory_status_enum` to `advisory` table
- [ ] Migration backfills `status` column from existing `status_id` join data
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is fully reversible (down migration restores original schema)
- [ ] Migration is atomic (all-or-nothing within a single transaction)

## Test Requirements
- [ ] Run the up migration against a test database with existing advisory data and verify all advisories have correct enum status values
- [ ] Run the down migration and verify the original schema is restored with correct FK relationships
- [ ] Verify that a failed mid-migration (simulated) rolls back cleanly without leaving partial state

## Verification Commands
- `cargo run -p migration -- up` -- migration runs to completion without error
- `cargo run -p migration -- down` -- down migration restores original schema
- `psql -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'advisory' AND column_name = 'status'"` -- confirms enum column exists after up migration

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
