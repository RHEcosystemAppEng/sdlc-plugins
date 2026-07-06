## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create an atomic database migration that converts the `advisory_status` lookup table into a PostgreSQL enum column on the `advisory` table. The migration must:
1. Create the `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `advisory_status` join (`advisory.status_id` -> `advisory_status.status`)
4. Drop the `status_id` foreign key column from the `advisory` table
5. Drop the `advisory_status` lookup table

All steps must be within a single migration that rolls back entirely on failure.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- Migration module implementing the enum conversion

## Files to Modify
- `migration/src/lib.rs` -- Register the new migration module
- `migration/Cargo.toml` -- Add migration module dependency if needed

## Implementation Notes
- Follow the SeaORM migration pattern established in `migration/src/m0001_initial/mod.rs` for migration structure and conventions
- Use `sea_orm_migration::prelude::*` for migration traits and helpers
- Create the enum type using raw SQL: `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')` since SeaORM migrations support raw SQL execution
- Backfill the `status` column using: `UPDATE advisory SET status = advisory_status.status FROM advisory_status WHERE advisory.status_id = advisory_status.id`
- Set `NOT NULL` constraint on the `status` column after backfill completes
- The down migration must reverse all steps: recreate `advisory_status` table, add `status_id` column, backfill from enum, drop `status` column, drop enum type
- Per the non-functional requirements, the migration must be safe to run while the application is serving traffic -- consider using `ALTER TABLE ... ADD COLUMN` with a default to minimize table locks

Per CONVENTIONS.md §Framework: use SeaORM migration patterns for database schema changes.
Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's Rust migration file scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` -- Existing migration module demonstrating the project's SeaORM migration structure and conventions

## Acceptance Criteria
- [ ] The `advisory_status_enum` PostgreSQL type exists with values (New, Analyzing, Fixed, Rejected)
- [ ] The `advisory` table has a `status` column of type `advisory_status_enum`
- [ ] All existing advisory rows have their `status` column populated from the prior `advisory_status` join
- [ ] The `status_id` column is removed from the `advisory` table
- [ ] The `advisory_status` table is dropped
- [ ] The migration is fully reversible (down migration restores the original schema)
- [ ] The migration runs without downtime on a production-sized dataset

## Test Requirements
- [ ] Run the migration forward and verify schema changes are applied correctly
- [ ] Run the migration backward (down) and verify the original schema is restored
- [ ] Verify the backfill correctly maps all existing status_id values to enum values
- [ ] Verify the migration is atomic -- partial failure rolls back all changes

## Verification Commands
- `cargo run --bin migration -- up` -- migration applies successfully
- `cargo run --bin migration -- down` -- migration rolls back cleanly

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
