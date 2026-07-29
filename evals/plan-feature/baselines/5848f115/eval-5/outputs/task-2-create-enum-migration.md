## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that atomically transitions the advisory status storage from a lookup table to a PostgreSQL enum column. The migration must: (1) create the `advisory_status_enum` PostgreSQL enum type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the `status` column from the existing `advisory.status_id` join to `advisory_status.name`; (4) drop the `status_id` foreign key column from the `advisory` table; (5) drop the `advisory_status` lookup table. The entire migration must be atomic — if any step fails, all changes roll back.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — new migration module implementing the enum type creation, column addition, backfill, FK drop, and table drop

## Files to Modify
- `migration/src/lib.rs` — register the new `m0002_advisory_status_enum` migration module
- `migration/Cargo.toml` — add module path if needed by the migration framework

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure, `MigrationTrait` implementation, and `up`/`down` method signatures.
- The `up` method should execute all five schema changes in sequence within the same transaction. Use SeaORM's `manager.exec_stmt()` or raw SQL for enum type creation since SeaORM may not have native enum type DDL support.
- The backfill step must join `advisory.status_id` to `advisory_status.id` and map each `advisory_status.name` value to the corresponding enum variant. Use an `UPDATE ... SET status = (SELECT name FROM advisory_status WHERE id = advisory.status_id)` pattern with appropriate casting.
- The `down` method must reverse the migration: recreate the `advisory_status` table, add back the `status_id` column, backfill `status_id` from the enum column, and drop the `status` column and enum type.
- The migration must be safe to run while the application is serving traffic (zero-downtime requirement). Since this is a feature-branch workflow, the migration and code changes will land together, but the migration itself should not acquire exclusive locks for longer than necessary.
- Per the project's Key Conventions: SeaORM is used for database interactions. Reference the existing migration module for the correct trait implementations and method signatures.
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's migration file scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern demonstrating `MigrationTrait` implementation, `up`/`down` methods, and schema creation statements

## Acceptance Criteria
- [ ] The `advisory_status_enum` PostgreSQL type exists with exactly four values: `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] The `advisory.status` column exists with type `advisory_status_enum`
- [ ] All existing advisory rows have their `status` column populated correctly from the former `status_id` lookup
- [ ] The `advisory.status_id` column no longer exists
- [ ] The `advisory_status` table no longer exists
- [ ] The migration is reversible — running `down` restores the lookup table and `status_id` column

## Test Requirements
- [ ] Run the migration `up` against a test database with pre-existing advisory rows and verify the enum column is populated correctly
- [ ] Run the migration `down` and verify the lookup table and FK column are restored with correct data
- [ ] Verify that partial failure in any step causes a complete rollback (no partial schema state)

## Verification Commands
- `cargo run -p migration -- up` — migration completes without error
- `cargo run -p migration -- down` — rollback completes without error
- `psql -c "SELECT enumlabel FROM pg_enum JOIN pg_type ON pg_enum.enumtypid = pg_type.oid WHERE pg_type.typname = 'advisory_status_enum';"` — returns New, Analyzing, Fixed, Rejected

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
