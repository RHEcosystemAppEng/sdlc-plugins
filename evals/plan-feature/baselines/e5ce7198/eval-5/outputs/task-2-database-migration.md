## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a database migration that introduces the `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), adds a `status` enum column to the `advisory` table backfilled from the existing `status_id` join, drops the `status_id` foreign key column, and drops the `advisory_status` lookup table. The migration must be atomic and reversible.

## Files to Create
- `migration/src/m0002_drop_status_table/mod.rs` -- migration to create enum type, add column, backfill, drop FK, drop table

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module

## Implementation Notes
Follow the existing migration module pattern in `migration/src/m0001_initial/mod.rs`. The migration should execute the following steps in order within a single transaction:
1. Create the `advisory_status_enum` PostgreSQL enum type with values `'New', 'Analyzing', 'Fixed', 'Rejected'`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the `advisory_status` table via `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)`
4. Set the `status` column to NOT NULL after backfill
5. Drop the `status_id` foreign key constraint and column from `advisory`
6. Drop the `advisory_status` table

The down migration must reverse these steps: recreate the `advisory_status` table, add `status_id` back, backfill from the enum column, drop the `status` column, and drop the enum type.

Per CONVENTIONS.md §Migration Patterns (if applicable): ensure indexes are created for any new columns used in query filtering. The `status` column will be used in WHERE clauses for advisory list filtering.
Applies: task modifies `migration/src/m0002_drop_status_table/mod.rs` matching the convention's migration file scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` -- reference for migration structure, table creation/modification patterns, and SeaORM migration API usage

## Acceptance Criteria
- [ ] `advisory_status_enum` PostgreSQL enum type exists with values New, Analyzing, Fixed, Rejected
- [ ] `advisory.status` column exists as NOT NULL enum type
- [ ] `advisory.status` values are correctly backfilled from the old `advisory_status` lookup table
- [ ] `advisory.status_id` column and foreign key constraint are dropped
- [ ] `advisory_status` table is dropped
- [ ] Migration is reversible (down migration restores the previous schema)
- [ ] Migration is atomic (all steps in a single transaction)

## Test Requirements
- [ ] Run migration up against a test database with existing advisory data and verify `status` column is populated correctly
- [ ] Run migration down and verify `advisory_status` table and `status_id` column are restored
- [ ] Verify migration handles empty `advisory` table without errors

## Verification Commands
- `cargo run --bin migration -- up` -- migration applies successfully
- `cargo run --bin migration -- down` -- migration rolls back successfully

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "High"}, "fixVersions": [{"name": "RHTPA 2.0.0"}]}

[sdlc-workflow] Description digest: sha256-md:cddb3408516a3b96f4e548df2c29f63f8f2f31c1162b9fe8dabf7ae5ebdd8a90
