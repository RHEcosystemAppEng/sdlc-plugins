## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be atomic: it creates the enum type, adds the enum column, backfills existing data from the `status_id` join, drops the foreign key column, and drops the lookup table in a single transaction. The migration must also be reversible to satisfy the requirement that if any step fails, the entire migration rolls back.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — Migration module that creates the `advisory_status_enum` type, adds the `status` column to `advisory`, backfills from the `advisory_status` join, drops `status_id`, and drops the `advisory_status` table. The down migration reverses all steps.

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration list

## Implementation Notes
Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and conventions. The migration must:
1. Create enum type: `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
2. Add column: `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`
3. Backfill: `UPDATE advisory SET status = s.name::advisory_status_enum FROM advisory_status s WHERE advisory.status_id = s.id`
4. Set NOT NULL: `ALTER TABLE advisory ALTER COLUMN status SET NOT NULL`
5. Drop FK column: `ALTER TABLE advisory DROP COLUMN status_id`
6. Drop lookup table: `DROP TABLE advisory_status`
7. Drop is last to ensure referential integrity during backfill

The down migration must reverse these steps in order: recreate the lookup table, add status_id column, backfill from enum, drop the enum column, drop the enum type.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` enum column to `advisory` table
- [ ] Migration backfills `status` from existing `advisory_status` join data
- [ ] Migration drops `status_id` foreign key column from `advisory`
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is reversible (down migration restores original schema)
- [ ] All steps execute in a single transaction (atomic)
- [ ] Migration module is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration applies successfully on a database with existing advisory data
- [ ] After migration, `advisory.status` contains correct enum values matching previous `advisory_status` names
- [ ] Down migration restores the original schema with `advisory_status` table and `status_id` foreign key
- [ ] Migration rolls back completely if any step fails (no partial state)

## Verification Commands
- `cargo test -p migration` — migration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
