## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must:
1. Create the `advisory_status_enum` PostgreSQL enum type with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the new `status` column from the existing `advisory_status` join (`advisory.status_id` → `advisory_status.id` → `advisory_status.name`)
4. Drop the `status_id` foreign key column from the `advisory` table
5. Drop the `advisory_status` lookup table

The migration must be atomic (all steps in a single transaction) and reversible.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration module implementing the enum type creation, column addition, data backfill, FK drop, and table drop

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration list

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and SeaORM migration trait implementation
- Use `sea_orm_migration::prelude::*` and implement `MigrationTrait` with `up` and `down` methods
- The `up` method should execute all five steps in order within a single migration (SeaORM runs each migration in a transaction by default)
- The `down` method should reverse the process: recreate the `advisory_status` table, add `status_id` column, backfill from enum, drop enum column, drop enum type
- Use raw SQL via `manager.get_connection().execute_unprepared()` for PostgreSQL enum type creation (`CREATE TYPE advisory_status_enum AS ENUM (...)`) since SeaORM's schema builder does not natively support PostgreSQL enums
- For the backfill step, use an `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum` pattern
- Per CONVENTIONS.md §Framework: use SeaORM migration infrastructure for all schema changes.
  Applies: task modifies `migration/src/lib.rs` matching the convention's migration file scope.

## Acceptance Criteria
- [ ] `advisory_status_enum` PostgreSQL type exists with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] `advisory` table has a `status` column of type `advisory_status_enum`
- [ ] All existing advisory rows have their `status` column populated from the former `advisory_status` lookup
- [ ] `status_id` column no longer exists on the `advisory` table
- [ ] `advisory_status` table no longer exists in the database
- [ ] Migration is reversible: running `down` restores the lookup table and FK column

## Test Requirements
- [ ] Migration `up` succeeds on a database with existing advisory rows and advisory_status data
- [ ] Migration `down` succeeds and restores the original schema
- [ ] Backfill correctly maps all four status values
- [ ] Migration fails atomically if any step encounters an error (no partial state)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
