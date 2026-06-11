# Task 2 — Create migration to replace advisory_status table with enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be atomic: if any step fails, the entire migration rolls back. The migration must be safe to run while the application is serving traffic (zero downtime).

The migration performs these steps in order:
1. Create the `advisory_status_enum` PostgreSQL enum type with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = advisory_status.name FROM advisory_status WHERE advisory.status_id = advisory_status.id`)
4. Set the `status` column to `NOT NULL` after backfill
5. Drop the `status_id` foreign key constraint and column from the `advisory` table
6. Drop the `advisory_status` table

The down migration must reverse all steps to restore the original schema.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration module implementing the enum column migration

## Files to Modify
- `migration/src/lib.rs` — register the new migration module

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and conventions
- Use SeaORM's migration framework (`MigrationTrait` with `up` and `down` methods)
- The backfill must happen within the same transaction as the column addition to ensure atomicity
- Use `ALTER TYPE ... ADD VALUE` syntax for PostgreSQL enum creation — note that this cannot be run inside a transaction in PostgreSQL < 12, but SeaORM migrations typically handle this
- Ensure the down migration re-creates the `advisory_status` table with its original schema and re-populates it from the enum column before dropping the enum type
- Per docs/constraints.md §2 (Commit Rules): commit must reference TC-9005 in the footer and follow Conventional Commits format
- Per docs/constraints.md §5 (Code Change Rules): inspect existing migration code before implementing

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — reference implementation for migration structure, table creation/modification patterns, and SeaORM migration conventions

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` enum column to `advisory` table
- [ ] Migration backfills `status` column from existing `advisory_status` join
- [ ] Migration sets `status` column to NOT NULL after backfill
- [ ] Migration drops `status_id` FK column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is reversible (down migration restores original schema)
- [ ] Migration is atomic (partial failure rolls back all changes)

## Test Requirements
- [ ] Migration runs successfully against a clean database
- [ ] Migration runs successfully against a database with existing advisory data (backfill works correctly)
- [ ] Down migration successfully restores the original schema
- [ ] Verify enum values match expected set: New, Analyzing, Fixed, Rejected

## Verification Commands
- `cargo run --bin migration -- up` — migration applies successfully
- `cargo run --bin migration -- down` — migration reverses successfully

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
