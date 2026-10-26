## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must:

1. Create the `advisory_status_enum` PostgreSQL enum type with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the new `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = s.name FROM advisory_status s WHERE advisory.status_id = s.id`)
4. Set the `status` column to NOT NULL after backfill
5. Drop the `status_id` foreign key constraint and column from the `advisory` table
6. Drop the `advisory_status` lookup table

The down migration must reverse all steps to restore the lookup table approach.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration implementing the enum type creation, column addition, backfill, FK drop, and table drop

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration runner

## Implementation Notes
The migration must be atomic: if any step fails, the entire migration rolls back. Use a single `manager.exec_stmt()` transaction or SeaORM's migration transaction support to ensure atomicity.

Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`. The migration struct should implement `MigrationTrait` with both `up` and `down` methods.

For the enum type creation, use raw SQL via `manager.get_connection().execute_unprepared()`:
```sql
CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected');
```

For the backfill, use a single UPDATE statement joining the lookup table before dropping it. This ensures zero-downtime compatibility — the application can continue reading the `status_id` column until the migration completes and the new code is deployed.

The non-functional requirement states the migration must be safe to run while the application is serving traffic. Ensure the `ALTER TABLE ADD COLUMN` uses a default or is nullable during backfill, then set NOT NULL after the backfill completes.

Per CONVENTIONS.md: follow the established migration module structure with `MigrationTrait` implementation.
Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's migration file scope.

## Acceptance Criteria
- [ ] The `advisory_status_enum` PostgreSQL type is created with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] The `advisory.status` column exists and is of type `advisory_status_enum`
- [ ] All existing advisory rows have their `status` column populated from the `advisory_status` lookup table join
- [ ] The `advisory.status` column is NOT NULL after backfill
- [ ] The `advisory.status_id` foreign key column is dropped
- [ ] The `advisory_status` table is dropped
- [ ] The down migration restores the `advisory_status` table, re-creates the FK column, backfills from the enum, and drops the enum type
- [ ] The migration runs successfully against a database with existing advisory data

## Test Requirements
- [ ] Run the up migration against a test database with sample advisory data and verify all rows are backfilled correctly
- [ ] Run the down migration and verify the lookup table and FK are restored
- [ ] Verify the migration is idempotent — running it twice does not cause errors
- [ ] Verify the enum type contains exactly the four expected values

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without errors
- `cargo run --bin migration -- down` — migration rolls back without errors
- `psql -c "SELECT enum_range(NULL::advisory_status_enum)"` — returns {New,Analyzing,Fixed,Rejected}

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
