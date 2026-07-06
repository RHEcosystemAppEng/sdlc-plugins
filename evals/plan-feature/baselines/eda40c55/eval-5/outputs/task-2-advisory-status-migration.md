## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that converts the advisory status storage from a lookup table to a PostgreSQL enum column. The migration must:
1. Create the `advisory_status_enum` PostgreSQL enum type with values (`New`, `Analyzing`, `Fixed`, `Rejected`).
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table.
3. Backfill the `status` column from the existing `status_id` foreign key join with `advisory_status`.
4. Drop the `status_id` foreign key column from the `advisory` table.
5. Drop the `advisory_status` lookup table.

The migration must be atomic (all steps succeed or all roll back) and safe to run while the application is serving traffic (zero downtime).

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration module implementing the enum conversion

## Files to Modify
- `migration/src/lib.rs` — register the new migration module
- `migration/Cargo.toml` — add any needed dependencies for enum support

## Implementation Notes
- Use SeaORM migration framework (`sea_orm_migration::prelude::*`) to define the migration.
- The `up` method must execute the five steps in order within a single migration. The `down` method must reverse them: recreate `advisory_status` table, add `status_id` column, backfill from enum, drop `status` column, drop enum type.
- Use raw SQL via `manager.get_connection().execute_unprepared()` for creating the PostgreSQL enum type, as SeaORM's schema builder does not natively support `CREATE TYPE ... AS ENUM`.
- For the backfill step, use a single `UPDATE advisory SET status = ... FROM advisory_status WHERE advisory.status_id = advisory_status.id` statement rather than row-by-row iteration.
- Per CONVENTIONS.md §Module pattern: follow the established migration module structure as seen in `migration/src/m0001_initial/mod.rs`.
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's migration file scope.
- Per CONVENTIONS.md §Framework: use SeaORM migration APIs for all DDL operations, falling back to raw SQL only for PostgreSQL-specific syntax (enum type creation).
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — reference for migration structure, table creation/drop patterns, and SeaORM migration API usage

## Acceptance Criteria
- [ ] `advisory_status_enum` PostgreSQL type exists with values (New, Analyzing, Fixed, Rejected)
- [ ] `advisory.status` column exists with type `advisory_status_enum`
- [ ] All existing advisory rows have `status` populated from the previous `status_id` join
- [ ] `advisory.status_id` column is dropped
- [ ] `advisory_status` table is dropped
- [ ] Migration `down` method successfully reverses all changes
- [ ] Migration is atomic — partial failure rolls back all changes

## Test Requirements
- [ ] Run migration `up` against a test database with seeded advisory and advisory_status data; verify enum type, column, and backfilled values
- [ ] Run migration `down` after `up`; verify advisory_status table and status_id column are restored with correct data
- [ ] Verify migration handles empty advisory table (no rows to backfill)
- [ ] Verify migration handles all four status values correctly during backfill

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without error
- `cargo run --bin migration -- down` — rollback completes without error
- `psql -c "SELECT enum_range(NULL::advisory_status_enum)"` — returns {New,Analyzing,Fixed,Rejected}

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
