## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be atomic and reversible: create the `advisory_status_enum` type, add the `status` enum column, backfill from the existing `status_id` join, drop the `status_id` foreign key column, and drop the `advisory_status` lookup table. All steps must execute within a single transaction to prevent inconsistent state.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — New migration implementing the enum type creation, column addition, data backfill, FK removal, and table drop

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration runner
- `migration/Cargo.toml` — Add migration module to the crate if needed

## Implementation Notes
The migration follows the existing pattern in `migration/src/m0001_initial/mod.rs`. Use SeaORM migration traits (`MigrationTrait`, `up`, `down` methods). The `up` method should:
1. Create the `advisory_status_enum` PostgreSQL enum type with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column by joining `advisory.status_id` to `advisory_status.id`
4. Drop the `status_id` foreign key constraint and column from `advisory`
5. Drop the `advisory_status` table

The `down` method must reverse all steps to ensure reversibility.

Per CONVENTIONS.md §Error Handling: wrap fallible migration steps with `.context()` for clear error messages. Applies: task modifies `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's `.rs` file scope.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` enum column to the `advisory` table
- [ ] Migration backfills the `status` column from the existing `status_id` foreign key join
- [ ] Migration drops the `status_id` column and its foreign key constraint from `advisory`
- [ ] Migration drops the `advisory_status` lookup table
- [ ] Migration is reversible (down method restores the previous schema)
- [ ] All steps execute atomically within a single transaction

## Test Requirements
- [ ] Run the migration against an empty database and verify the schema matches expectations
- [ ] Run the migration against a database with existing advisory rows and verify data is backfilled correctly
- [ ] Run the down migration and verify the original schema is restored
- [ ] Verify the migration handles all four status values correctly during backfill

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
