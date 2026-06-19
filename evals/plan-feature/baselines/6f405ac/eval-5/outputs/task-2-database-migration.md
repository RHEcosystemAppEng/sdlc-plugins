# Task 2 — Create database migration to replace advisory_status table with enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a SeaORM migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be atomic and reversible. Steps within the migration: (1) create the `advisory_status_enum` PostgreSQL enum type with values New, Analyzing, Fixed, Rejected; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the `status` column from the existing `advisory_status` join; (4) set `status` column to NOT NULL after backfill; (5) drop the `status_id` foreign key column from `advisory`; (6) drop the `advisory_status` table.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration module implementing up() and down() for the enum migration

## Files to Modify
- `migration/src/lib.rs` — register the new migration module
- `migration/Cargo.toml` — add any needed dependencies if required

## Implementation Notes
Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and conventions. The migration must execute all steps within a single transaction to ensure atomicity -- if any step fails, the entire migration rolls back. The down() method must reverse all steps: recreate the `advisory_status` table, add back the `status_id` FK column, backfill from the enum column, drop the `status` column, and drop the enum type.

Use SeaORM migration API for creating the enum type, adding/dropping columns, and dropping tables. Reference the SeaORM `sea_query` extension methods for PostgreSQL enum types.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` enum column to `advisory` table
- [ ] Migration backfills `status` from existing `status_id` join in the same transaction
- [ ] Migration sets `status` column to NOT NULL after backfill
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is reversible via down() method
- [ ] All steps execute within a single transaction (atomic)

## Test Requirements
- [ ] Migration applies successfully against a database with existing advisory rows containing all four status values
- [ ] Migration rollback (down) restores the original schema with advisory_status table and status_id FK
- [ ] After migration, advisory table has `status` column of enum type and no `status_id` column

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without error
- `cargo run --bin migration -- down` — migration rolls back without error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
