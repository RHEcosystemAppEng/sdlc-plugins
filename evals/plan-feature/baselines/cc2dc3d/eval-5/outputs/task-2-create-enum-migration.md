# Task 2 — Create migration to add advisory_status_enum and migrate data

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a new SeaORM migration that performs the full schema transition from the `advisory_status` lookup table to an `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The migration must be atomic and reversible: if any step fails, the entire migration rolls back. The migration performs four operations in sequence: (1) create the `advisory_status_enum` type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table and backfill it from the existing `advisory_status` join; (3) drop the `status_id` foreign key column from `advisory`; (4) drop the `advisory_status` table.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — New migration module implementing the enum type creation, column addition with backfill, FK column drop, and table drop

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration runner

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and conventions.
- The migration must implement both `up()` and `down()` methods for reversibility. The `down()` method should recreate the `advisory_status` table, re-add the `status_id` FK column, backfill from the enum column, and drop the enum type.
- Use SeaORM's `manager.exec_stmt()` or raw SQL for PostgreSQL-specific operations like `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`.
- The backfill step should use a single UPDATE statement joining `advisory` with `advisory_status` to populate the new `status` column from the existing `status_id` values.
- Ensure the migration is safe for zero-downtime deployment: the enum column should be added as nullable first, backfilled, then set to NOT NULL before dropping the old column.
- The non-functional requirement states the migration must be atomic — wrap all operations in a single transaction (SeaORM migrations run in transactions by default).

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Existing migration pattern showing SeaORM migration structure, table/column creation, and index management

## Acceptance Criteria
- [ ] `advisory_status_enum` PostgreSQL type is created with exactly four values: `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] `advisory.status` column exists with type `advisory_status_enum` and is NOT NULL after backfill
- [ ] All existing advisory rows have their `status` column populated correctly from the old `status_id` join
- [ ] `advisory.status_id` foreign key column is dropped
- [ ] `advisory_status` table is dropped
- [ ] Migration is reversible — `down()` restores the previous schema
- [ ] Migration runs successfully against a database with existing advisory data

## Test Requirements
- [ ] Run the migration `up()` against a test database with seeded advisory data and verify all four operations complete
- [ ] Run the migration `down()` and verify the schema is restored to its original state
- [ ] Verify the backfill correctly maps all existing `status_id` values to the corresponding enum values
- [ ] Verify the migration fails atomically if any step encounters an error (e.g., duplicate enum type)

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without errors
- `cargo run --bin migration -- down` — rollback completes without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
