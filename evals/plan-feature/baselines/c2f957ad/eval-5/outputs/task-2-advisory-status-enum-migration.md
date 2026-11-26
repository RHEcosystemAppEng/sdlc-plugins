## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Add a single, atomic, reversible SeaORM migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must:

1. Create the PostgreSQL enum type `advisory_status_enum` with values `New`, `Analyzing`, `Fixed`, `Rejected`.
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table.
3. Backfill `advisory.status` from the existing `advisory.status_id` -> `advisory_status(id)` join in the same migration.
4. Drop the `status_id` foreign key constraint and column from `advisory` (only after the backfill completes).
5. Drop the `advisory_status` lookup table (only after all references are removed).

The `down` migration must reverse every step (recreate `advisory_status`, re-seed its four rows, re-add `status_id`, backfill it from `status`, drop `status`, drop the enum type). This is part of feature TC-9005 and is the schema foundation that all other TC-9005 tasks build on.

## Files to Modify
- `migration/src/lib.rs` — register the new migration in the `Migrator` migrations list, after `m0001_initial`

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — new migration implementing the enum type, column add, backfill, FK/column drop, table drop, and the full reverse `down` path

## Implementation Notes
- Follow the existing migration module layout in `migration/src/m0001_initial/mod.rs` (one directory per migration with a `mod.rs` implementing `MigrationTrait` with `up`/`down`), and register it the same way `m0001_initial` is registered in `migration/src/lib.rs`.
- The `advisory_status` table and the `advisory.status_id` FK are defined in `migration/src/m0001_initial/mod.rs`. Do NOT edit the already-applied `m0001_initial` migration — dropping the table is done forward-only in the new migration so existing databases upgrade cleanly. (The feature goal "remove the `advisory_status` table and its migration history" is interpreted as "the table no longer exists after migrating"; rewriting applied migration history is out of scope — see impact map open question.)
- **Atomicity (fail-closed):** the feature requires that a partial migration (enum column present but lookup table already dropped, or vice versa) never be left behind. Execute all steps inside a single transaction (PostgreSQL supports transactional DDL; ensure the migration is not marked to run outside a transaction). Do not swallow errors from any step — every `manager.exec_stmt(...)` / `execute_unprepared(...)` result must be propagated with `?` so that a failing step aborts and rolls back the whole migration.
- **Backfill must not silently produce NULL/default statuses:** after the `UPDATE advisory SET status = ...::advisory_status_enum FROM advisory_status WHERE advisory.status_id = advisory_status.id`, verify that no row has `status IS NULL` where `status_id` was non-NULL (e.g., `SELECT count(*) ... ` and return a `DbErr::Migration(...)` if non-zero) before dropping `status_id`. Then set `status` to `NOT NULL` if `status_id` was `NOT NULL` in `m0001_initial`. An unmapped lookup value (e.g., a status name in `advisory_status` that is not one of the four enum labels) must fail the migration, not be defaulted.
- Use `sea_orm_migration::prelude::extension::postgres::Type` (`Type::create().as_enum(...).values([...])`) for the enum type and `Type::drop()` in `down`, so the code stays within the SeaORM migration DSL used by the existing migration; use raw SQL (`execute_unprepared`) only for the backfill `UPDATE ... FROM` statement.
- **Zero downtime:** keep the migration to metadata DDL plus one set-based `UPDATE`; avoid per-row loops. Note in the PR description that the migration must be tested against a production-sized dataset before deployment (Customer Considerations).
- Commit rules (docs/constraints.md §2): Conventional Commits format (e.g., `feat(migration): replace advisory_status table with enum column`), footer `Implements <task-key>`, and an `Assisted-by:` trailer.
- PR rules (docs/constraints.md §3): open the PR with `gh pr create --base TC-9005`; post the PR link as a comment on this Jira task.
- Code change rules (docs/constraints.md §5): limit changes to the files listed above; inspect `migration/src/m0001_initial/mod.rs` before writing the new migration; reuse the existing migration DSL rather than introducing new helpers.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration showing the `MigrationTrait` `up`/`down` structure and the original `advisory_status` / `advisory.status_id` definitions that the `down` path must recreate exactly
- `migration/src/lib.rs::Migrator` — existing migration registry to extend

## Acceptance Criteria
- [ ] PostgreSQL enum type `advisory_status_enum` exists with exactly the values `New`, `Analyzing`, `Fixed`, `Rejected` after `up`
- [ ] `advisory.status` column of type `advisory_status_enum` exists and every pre-existing advisory row has `status` equal to the name of its former `advisory_status` row
- [ ] `advisory.status_id` column and its FK constraint no longer exist after `up`
- [ ] `advisory_status` table no longer exists after `up`
- [ ] The migration is atomic: if any step fails (including the backfill verification), the migration returns an error and the database is left exactly in its pre-migration state (no enum column without the table, no dropped table without the enum column)
- [ ] The backfill fails closed: an `advisory_status` value that does not map to an enum label causes the migration to error instead of writing NULL or a default
- [ ] `down` fully reverses the migration: `advisory_status` table restored with its four rows, `advisory.status_id` restored and backfilled, `advisory.status` and `advisory_status_enum` removed
- [ ] The migration is registered in `migration/src/lib.rs` after `m0001_initial`

## Test Requirements
- [ ] Migration test: seed advisories with each of the four statuses under the old schema, run `up`, and assert each row's `status` enum value matches its original status name
- [ ] Migration test: run `up` then `down`, and assert the `advisory_status` table, its four rows, and `advisory.status_id` values are restored and `advisory_status_enum` no longer exists
- [ ] Fail-closed test: seed an `advisory_status` row with a name outside the enum set (or force a step to fail), run `up`, assert the migration returns an error AND that `advisory_status` still exists, `advisory.status_id` still exists, and `advisory.status` does not exist (full rollback, no partial state)
- [ ] Test that `up` on an empty `advisory` table succeeds

## Verification Commands
- `cargo test -p migration` — all migration tests pass
- `cargo run -p migration -- up && cargo run -p migration -- down` — both directions complete without error against a local PostgreSQL

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
