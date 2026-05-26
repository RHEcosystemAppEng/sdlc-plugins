# Task 2 — Create migration to replace advisory_status table with enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a new SeaORM database migration that replaces the `advisory_status` lookup table with an `advisory_status_enum` PostgreSQL enum column directly on the `advisory` table. The migration must be atomic (all-or-nothing) and reversible. It performs the following steps in order: create the enum type, add the enum column, backfill from the existing join, drop the foreign key column, and drop the lookup table.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — New migration module implementing the enum migration

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration runner
- `migration/Cargo.toml` — Add any needed dependencies if not already present

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for structure and naming conventions.
- The migration up() must execute these steps in order:
  1. `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
  2. `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`
  3. `UPDATE advisory SET status = s.name::advisory_status_enum FROM advisory_status s WHERE advisory.status_id = s.id` (backfill)
  4. `ALTER TABLE advisory ALTER COLUMN status SET NOT NULL` (after backfill)
  5. `ALTER TABLE advisory DROP COLUMN status_id` (removes FK constraint implicitly)
  6. `DROP TABLE advisory_status`
- The migration down() must reverse all steps: recreate the lookup table, re-add the FK column, backfill status_id from the enum, drop the enum column, drop the enum type.
- Use raw SQL via `manager.get_connection().execute_unprepared()` for the enum type creation since SeaORM's schema manager does not natively support PostgreSQL enum type DDL.
- The migration must be safe to run while the application is serving traffic (zero downtime requirement). Consider that the backfill UPDATE and column operations should be fast on reasonable table sizes.
- Per constraints doc section 2 (Commit Rules): commit message must reference TC-9005 and follow Conventional Commits format.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Existing migration demonstrating the project's migration structure and SeaORM migration trait implementation pattern

## Acceptance Criteria
- [ ] Migration up() creates the `advisory_status_enum` type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration up() adds a `status` column of type `advisory_status_enum` to the `advisory` table
- [ ] Migration up() backfills the `status` column from the existing `advisory_status` join
- [ ] Migration up() drops the `status_id` column from the `advisory` table
- [ ] Migration up() drops the `advisory_status` table
- [ ] Migration down() fully reverses all changes (recreates table, column, backfills, drops enum)
- [ ] Migration is atomic — partial failure rolls back all changes
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration runs successfully against a test database with existing advisory data using various statuses
- [ ] Migration rollback (down) restores the original schema with data integrity preserved
- [ ] Verify the `advisory_status_enum` type exists after migration with exactly four values

## Verification Commands
- `cargo run -p migration -- up` — migration completes without errors
- `cargo run -p migration -- down` — rollback completes without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
