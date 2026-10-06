## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that converts the advisory status storage from a lookup table (`advisory_status`) to a PostgreSQL enum column on the `advisory` table. The migration must be atomic: if any step fails, the entire migration rolls back. The migration performs four operations in sequence: (1) create the `advisory_status_enum` PostgreSQL enum type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table and backfill it from the existing `advisory_status` join; (3) drop the `status_id` foreign key column from `advisory`; (4) drop the `advisory_status` lookup table. The down migration must reverse these steps in order.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — reversible migration implementing the enum type creation, column addition with backfill, FK column drop, and lookup table drop

## Files to Modify
- `migration/src/lib.rs` — register the new migration module `m0002_advisory_status_enum`
- `migration/Cargo.toml` — add dependencies if needed for enum type support in SeaORM migrations

## Implementation Notes
- Use SeaORM's migration framework to define `up` and `down` functions in the migration module.
- The `up` function should: (1) execute raw SQL to create the enum type `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`; (2) add the `status` column with `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`; (3) backfill with `UPDATE advisory SET status = s.name::advisory_status_enum FROM advisory_status s WHERE advisory.status_id = s.id`; (4) set `NOT NULL` constraint on `status`; (5) drop the `status_id` column; (6) drop the `advisory_status` table.
- The `down` function must reverse all steps: recreate `advisory_status` table, add `status_id` column, backfill from enum, drop `status` column, drop the enum type.
- For zero-downtime safety, the migration should be wrapped in a single transaction (SeaORM migrations are transactional by default).
- Reference the existing migration pattern in `migration/src/m0001_initial/mod.rs` for the established migration structure.
- Per CONVENTIONS.md §Framework: use SeaORM migration API for all DDL operations.
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's Rust file scope.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with exactly four values: `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] Migration adds `status` column of type `advisory_status_enum` to `advisory` table
- [ ] Migration backfills `status` column from existing `advisory_status` join data
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is reversible — `down` function restores the previous schema
- [ ] Migration is atomic — partial failure rolls back all changes
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Run migration `up` against a test database with existing advisory data and verify enum column is populated correctly
- [ ] Run migration `down` and verify the lookup table and FK column are restored
- [ ] Verify migration handles empty `advisory` table (no rows to backfill)
- [ ] Verify migration handles all four status values correctly during backfill

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without error
- `cargo run --bin migration -- down` — rollback completes without error
- `psql -c "SELECT enum_range(NULL::advisory_status_enum)"` — returns `{New,Analyzing,Fixed,Rejected}`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
