## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a database migration that performs the full schema transformation from the `advisory_status` lookup table to an enum column on the `advisory` table. The migration must:

1. Create the PostgreSQL enum type `advisory_status_enum` with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a new `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = advisory_status.name FROM advisory_status WHERE advisory.status_id = advisory_status.id`)
4. Set `NOT NULL` constraint on the `status` column after backfill
5. Drop the `status_id` foreign key column from the `advisory` table
6. Drop the `advisory_status` lookup table

The migration must be reversible (down migration recreates the lookup table, re-adds the FK column, and backfills from the enum column).

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration module implementing the enum type creation, column addition, backfill, FK drop, and table drop

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migrator's migration list

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and SeaORM migration traits
- Use `sea_orm_migration::prelude::*` and implement `MigrationTrait` with `up` and `down` methods
- The backfill must happen within the same migration transaction to ensure atomicity
- Use raw SQL for the PostgreSQL enum type creation (`CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`) since SeaORM migrations support raw SQL via `manager.get_connection().execute_unprepared()`
- Per the feature's non-functional requirements: the migration must be atomic — if any step fails, the entire migration rolls back
- Zero downtime requirement: use `ADD COLUMN ... DEFAULT` pattern to avoid full table lock on column addition
- The down migration must: recreate `advisory_status` table, re-add `status_id` FK column, backfill FK references from enum values, drop the `status` column, and drop the enum type

## Acceptance Criteria
- [ ] PostgreSQL enum type `advisory_status_enum` exists with values (New, Analyzing, Fixed, Rejected)
- [ ] `advisory` table has a `status` column of type `advisory_status_enum` with NOT NULL constraint
- [ ] All existing advisory rows have `status` populated from the former `advisory_status` join
- [ ] `status_id` column is removed from `advisory` table
- [ ] `advisory_status` table is dropped
- [ ] Down migration successfully reverses all changes

## Test Requirements
- [ ] Migration runs successfully on a fresh database
- [ ] Migration runs successfully on a database with existing advisory data
- [ ] Down migration successfully reverses the migration
- [ ] Backfill correctly maps all four status values
- [ ] Migration is atomic — partial failures result in full rollback

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without errors
- `cargo run --bin migration -- down` — down migration completes without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
