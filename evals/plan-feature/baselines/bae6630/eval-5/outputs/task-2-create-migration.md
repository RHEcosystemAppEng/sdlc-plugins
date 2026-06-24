## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a SeaORM database migration that atomically transitions the advisory status from a lookup table to a PostgreSQL enum column. The migration must: create the `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected); add a `status` enum column to the `advisory` table; backfill the `status` column from the existing `advisory_status` join; drop the `status_id` foreign key column from `advisory`; and drop the `advisory_status` lookup table. All steps must execute within a single transaction so a failure at any point rolls back the entire migration.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — Migration module implementing the enum conversion

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migrator

## Implementation Notes
Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and conventions. The migration must:

1. Use `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')` to define the PostgreSQL enum type.
2. Add the `status` column as `advisory_status_enum` to the `advisory` table.
3. Backfill: `UPDATE advisory SET status = s.name::advisory_status_enum FROM advisory_status s WHERE advisory.status_id = s.id`.
4. Set the `status` column to `NOT NULL` after backfill.
5. Drop the `status_id` foreign key constraint and column from `advisory`.
6. Drop the `advisory_status` table.
7. Implement a `down()` migration that reverses all steps for reversibility.

The migration module in `migration/src/lib.rs` registers all migrations — add the new module to the migration list following the pattern used for `m0001_initial`.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` enum column to `advisory` table and backfills from lookup table join
- [ ] Migration sets `status` column to NOT NULL after backfill
- [ ] Migration drops `status_id` FK column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] All migration steps execute within a single transaction (atomic rollback on failure)
- [ ] Down migration reverses all changes (recreates table, FK, drops enum type)
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration applies successfully against a clean database with existing advisory_status data
- [ ] Migration rolls back cleanly via down() migration
- [ ] Backfill correctly maps all existing status_id values to enum values

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

## Digest
[sdlc-workflow] Description digest: sha256-md:6cea714bf990a09cf984ef4429dcde771a6d430eeadb3a60d48cd2954493dfd9
