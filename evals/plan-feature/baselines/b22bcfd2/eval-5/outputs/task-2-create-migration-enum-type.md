## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a SeaORM migration that defines the `advisory_status_enum` PostgreSQL enum type, adds the `status` enum column to the `advisory` table with a backfill from the existing `status_id` join, drops the `status_id` foreign key column, and drops the `advisory_status` lookup table. All schema changes are in a single migration to ensure atomicity — if any step fails, the entire migration rolls back.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — new migration module: create enum type, add column, backfill, drop FK, drop table

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migrator's migration list
- `migration/Cargo.toml` — add any new dependencies if needed for enum support

## Implementation Notes
Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs`. The migration should:

1. Create the PostgreSQL enum type using `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')` via raw SQL in SeaORM's `manager.get_connection().execute_unprepared()`.
2. Add column `status` of type `advisory_status_enum` to the `advisory` table with a default of `'New'`.
3. Backfill the `status` column from the existing join: `UPDATE advisory SET status = s.name::advisory_status_enum FROM advisory_status s WHERE advisory.status_id = s.id`.
4. Drop the `status_id` foreign key constraint and column from `advisory`.
5. Drop the `advisory_status` table.
6. The `down()` migration should reverse all steps: recreate the lookup table, add `status_id` column, backfill from enum, drop enum column, drop enum type.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` type with values New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` column to `advisory` table and backfills from `status_id` join
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is reversible — `down()` restores the previous schema
- [ ] All steps are in a single transaction for atomicity

## Test Requirements
- [ ] Migration runs successfully against a test database with existing advisory data
- [ ] After migration, `advisory.status` contains the correct enum value for each row
- [ ] After migration, the `advisory_status` table no longer exists
- [ ] Rolling back the migration restores the `advisory_status` table and `status_id` column
- [ ] Migration handles edge case of NULL `status_id` values (if any exist)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005
