## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: (1) create the `advisory_status_enum` type with values (New, Analyzing, Fixed, Rejected), (2) add a `status` enum column to the `advisory` table, (3) backfill the `status` column from the existing `status_id` join, (4) drop the `status_id` foreign key column, and (5) drop the `advisory_status` lookup table. The migration must be atomic and reversible — if any step fails, the entire migration rolls back.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration module implementing the enum type creation, column addition, backfill, FK drop, and table drop

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration list
- `migration/Cargo.toml` — add any required dependencies for enum type handling if needed

## Implementation Notes
The migration should follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`. Use SeaORM's migration framework with `MigrationTrait` for both `up()` and `down()` methods.

In the `up()` method:
1. Execute raw SQL to create the enum type: `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
2. Add the `status` column with `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`
3. Backfill: `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum`
4. Set NOT NULL constraint on the new column after backfill
5. Drop the FK constraint and `status_id` column
6. Drop the `advisory_status` table

In the `down()` method: reverse all operations to restore the lookup table design.

Per CONVENTIONS.md §Module pattern: follow the established migration module structure in `migration/src/`.
Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's migration file scope.

Per CONVENTIONS.md §Framework: use SeaORM migration framework for database schema changes.
Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's Rust/SeaORM scope.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` enum column to `advisory` table
- [ ] Migration backfills `status` column from `advisory_status` join data
- [ ] Migration drops `status_id` FK column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration `down()` method reverses all changes (recreates table, FK, drops enum)
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration runs successfully against a test database with existing advisory data
- [ ] Migration rollback (`down()`) restores the original schema without data loss
- [ ] Backfill correctly maps all existing status_id values to enum values
- [ ] Migration handles empty advisory table gracefully

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
