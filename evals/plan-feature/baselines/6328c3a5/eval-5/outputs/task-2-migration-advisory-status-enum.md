## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a database migration that converts the advisory status storage from a lookup table (`advisory_status`) to a PostgreSQL enum column on the `advisory` table. The migration must be atomic and reversible: if any step fails, the entire migration rolls back. The migration must also be safe to run while the application is serving traffic (zero downtime).

The migration performs these steps in order:
1. Create the `advisory_status_enum` PostgreSQL enum type with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = ... FROM advisory_status WHERE advisory.status_id = advisory_status.id`)
4. Drop the `status_id` foreign key constraint and column from the `advisory` table
5. Drop the `advisory_status` lookup table

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- migration implementing all five steps with rollback support

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and registration.
- Use SeaORM's migration API (`sea_orm_migration::prelude::*`) for schema operations.
- The backfill step must use a single `UPDATE ... FROM` statement to populate the enum column from the join, ensuring atomicity.
- The `down()` method must reverse all steps: recreate `advisory_status` table, add `status_id` column, backfill from enum, drop enum column, drop enum type.
- Per the non-functional requirements: the migration must be wrapped in a transaction so that a failure at any step rolls back the entire migration.
- For zero-downtime safety: the enum type creation and column addition are non-blocking operations in PostgreSQL. The `UPDATE` backfill should be done in a way that minimizes lock duration.

Per CONVENTIONS.md §Error Handling: use `.context()` wrapping on fallible migration operations.
Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` -- existing migration showing the project's migration structure and SeaORM migration API usage

## Acceptance Criteria
- [ ] Migration `m0002_advisory_status_enum` creates the `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` column of type `advisory_status_enum` to the `advisory` table
- [ ] Migration backfills the `status` column from the `advisory_status` join
- [ ] Migration drops the `status_id` foreign key column from `advisory`
- [ ] Migration drops the `advisory_status` lookup table
- [ ] Migration `down()` method reverses all changes
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration `up()` runs successfully on a clean database
- [ ] Migration `down()` reverses all changes and restores the original schema
- [ ] Backfill correctly maps all existing status_id values to enum values
- [ ] Migration is atomic: partial failure rolls back all changes

## Verification Commands
- `cargo test -p migration` -- migration tests pass
- `sea-orm-cli migrate up` -- migration applies successfully

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
