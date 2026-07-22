## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a new SeaORM database migration that performs the full advisory status enum conversion in a single atomic transaction. The migration must: create the `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add a `status` enum column to the `advisory` table, backfill the `status` column from the existing `advisory_status` join, drop the `status_id` foreign key column from the `advisory` table, and drop the `advisory_status` lookup table. The migration must be reversible: the down migration recreates the lookup table, re-adds the foreign key column, backfills it from the enum column, and drops the enum type.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration list

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration implementing the enum conversion (up: create enum type, add column, backfill, drop FK, drop table; down: reverse all steps)

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and SeaORM migration trait implementation
- Use `manager.get_connection()` to execute raw SQL within the migration for creating the PostgreSQL enum type (`CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`)
- Backfill the `status` column using `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)`
- Set the `status` column to `NOT NULL` after backfill completes
- Drop the `status_id` column's foreign key constraint before dropping the column
- Ensure the entire migration runs within a single transaction for atomicity — if any step fails, all changes roll back
- The down migration must reverse all operations in the correct order: recreate `advisory_status` table, add `status_id` column, backfill from enum, drop `status` column, drop enum type

Per CONVENTIONS.md Key Conventions: follow the SeaORM migration pattern established in the codebase. Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's migration file scope.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` enum column to `advisory` table
- [ ] Migration backfills `status` column from the `advisory_status` join
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is reversible — down migration restores the previous schema
- [ ] All steps execute within a single atomic transaction
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Run the migration against a test database and verify the `advisory_status_enum` type exists
- [ ] Verify the `advisory.status` column contains correct values after backfill
- [ ] Verify the `advisory_status` table no longer exists after migration
- [ ] Run the down migration and verify the schema is restored to its original state
- [ ] Verify the migration rolls back cleanly if any step fails (simulate failure)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
