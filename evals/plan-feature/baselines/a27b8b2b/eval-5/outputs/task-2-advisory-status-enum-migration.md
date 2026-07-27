## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be atomic — if any step fails, the entire migration rolls back. The migration performs five operations in sequence: (1) create the `advisory_status_enum` type with values New, Analyzing, Fixed, Rejected; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = advisory_status.name FROM advisory_status WHERE advisory.status_id = advisory_status.id`); (4) drop the `status_id` foreign key column from `advisory`; (5) drop the `advisory_status` table.

The down migration must reverse these operations: recreate the `advisory_status` table, recreate the `status_id` FK column, backfill `status_id` from the enum column, drop the `status` column, and drop the `advisory_status_enum` type.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — reversible migration implementing the five-step enum migration

## Files to Modify
- `migration/src/lib.rs` — register the new migration module
- `migration/Cargo.toml` — add any required dependencies for enum type handling (if not already present)

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and naming conventions.
- Use SeaORM migration API: `sea_orm_migration::prelude::*` with `MigrationTrait` implementation.
- The migration must handle the backfill within the same transaction to ensure atomicity per the NFR: "if any step fails, the entire migration rolls back."
- For the enum type creation, use raw SQL via `manager.get_connection().execute_unprepared()` since SeaORM does not have native enum type creation support in migrations.
- Ensure the backfill query handles NULL `status_id` values gracefully (set a default enum value or reject rows with NULL status).
- The migration must be safe to run while the application is serving traffic (zero downtime requirement). Since this is a backfill + column add + column drop, consider using `ALTER TABLE ... ADD COLUMN ... DEFAULT` for the initial add to avoid table rewrites on supported PostgreSQL versions (11+).

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` type with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` column of type `advisory_status_enum` to `advisory` table
- [ ] Migration backfills `status` column from `advisory_status` join
- [ ] Migration drops `status_id` FK column from `advisory` table
- [ ] Migration drops `advisory_status` table
- [ ] Down migration reverses all operations and restores the original schema
- [ ] Migration is atomic — partial failure rolls back all changes
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Run the migration up against a test database and verify the `advisory_status_enum` type exists
- [ ] Verify the `status` column exists on `advisory` with correct type
- [ ] Verify the `advisory_status` table no longer exists after migration up
- [ ] Verify the `status_id` column no longer exists on `advisory` after migration up
- [ ] Run the migration down and verify the original schema is restored (lookup table, FK column)
- [ ] Verify backfill correctness: advisory rows have the correct enum value matching their original status

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without error
- `cargo run --bin migration -- down` — rollback completes without error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
