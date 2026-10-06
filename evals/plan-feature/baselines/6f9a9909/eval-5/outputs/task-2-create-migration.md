# Task 2 — Create database migration for advisory status enum conversion

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that converts the advisory status storage from a lookup table (`advisory_status`) to a PostgreSQL enum column on the `advisory` table. The migration must:

1. Create the `advisory_status_enum` PostgreSQL enum type with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `advisory_status` join (`advisory.status_id` -> `advisory_status.id`)
4. Drop the `status_id` foreign key column from the `advisory` table
5. Drop the `advisory_status` lookup table

The migration must be atomic (all steps succeed or all roll back) and safe to run while the application is serving traffic (zero downtime).

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration runner

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration implementing enum type creation, column addition, data backfill, FK column removal, and lookup table drop

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for the migration module structure
- Use SeaORM's `sea_orm_migration::prelude::*` for migration operations
- The `up()` method must execute all five steps in order within a single transaction
- The `down()` method must reverse the migration: recreate `advisory_status` table, recreate `status_id` FK column, backfill `status_id` from `status` enum, drop `status` column, drop `advisory_status_enum` type
- Use `extension::postgres::Type` for creating the PostgreSQL enum type
- Use raw SQL for the backfill step: `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum`
- Per CONVENTIONS.md §Framework: use SeaORM migration API for all DDL operations.
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's Rust database file scope.

### Constraints (from docs/constraints.md)
- §2.1: Every commit MUST reference Jira issue ID in the footer (e.g., `Implements TC-9005`)
- §2.2: Commit messages MUST follow Conventional Commits (`feat(migration): ...`)
- §2.3: Every commit MUST include `--trailer="Assisted-by: Claude Code"`
- §3.1: Feature branch MUST be named after the Jira issue ID (`TC-9005`)
- §5.1: Changes MUST be scoped to the files listed in Files to Modify and Files to Create

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration module demonstrating the project's migration structure, transaction handling, and DDL patterns

## Acceptance Criteria
- [ ] `advisory_status_enum` PostgreSQL type exists with values `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] `advisory.status` column exists with type `advisory_status_enum`
- [ ] All existing advisory rows have `status` populated from the former `status_id` join
- [ ] `advisory.status_id` column no longer exists
- [ ] `advisory_status` table no longer exists
- [ ] Migration is fully reversible (`down()` restores the previous schema)
- [ ] Migration runs without downtime on a live database

## Test Requirements
- [ ] Run migration `up()` against a test database with existing advisory rows and verify all rows have correct `status` values
- [ ] Run migration `down()` and verify the original schema (lookup table, FK column) is restored with correct data
- [ ] Verify the migration is idempotent — running `up()` when already applied does not error
- [ ] Verify enum type contains exactly four values: `New`, `Analyzing`, `Fixed`, `Rejected`

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without error
- `cargo run --bin migration -- down` — migration rolls back without error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
