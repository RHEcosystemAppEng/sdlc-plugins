**Summary:** Add advisory status enum migration (create type, backfill, drop FK column and lookup table)

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Add a new SeaORM migration that converts advisory lifecycle status from the `advisory_status` lookup table to a PostgreSQL enum column on `advisory`. The migration must:

1. Create the enum type `advisory_status_enum` with values `New`, `Analyzing`, `Fixed`, `Rejected`.
2. Add a `status` column of type `advisory_status_enum` to `advisory`.
3. Backfill `advisory.status` from the existing `advisory.status_id` → `advisory_status` join.
4. Make `advisory.status` `NOT NULL` after backfill.
5. Drop the `advisory.status_id` foreign key constraint and column.
6. Drop the `advisory_status` lookup table.

The migration must be atomic (all steps in one transaction — any failure rolls back everything) and reversible (the `down` migration restores the lookup table, its four rows, `advisory.status_id` with its FK and values, then drops `advisory.status` and the enum type).

Part of TC-9005: removes the join overhead on every advisory query.

## Files to Modify
- `migration/src/lib.rs` — register the new migration in the `Migrator` migrations list after `m0001_initial`

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — new migration implementing `up` (create enum, add/backfill column, drop FK column, drop table) and `down` (full reversal)

## Implementation Notes
- Follow the structure of the existing migration in `migration/src/m0001_initial/mod.rs` (a `Migration` struct implementing `MigrationTrait` with `up`/`down`) and the registration pattern in `migration/src/lib.rs`. Do not edit `m0001_initial` — historical migrations are immutable; the new migration supersedes the lookup table.
- Read `migration/src/m0001_initial/mod.rs` to confirm the exact names of the `advisory_status` table, its name/label column, the `advisory.status_id` column, and the FK constraint name before writing `drop_foreign_key` / `drop_column` statements.
- Atomicity: PostgreSQL DDL is transactional. Execute all `up` steps through the `SchemaManager` within a single transaction (e.g., `manager.get_connection().begin()` / or rely on SeaORM's per-migration transaction for Postgres) so a failure after the enum column is added but before the table is dropped leaves no partial state.
- Backfill (fail-closed): use a cast so unknown values fail the migration instead of silently producing NULLs:
  `UPDATE advisory a SET status = s.<name_col>::advisory_status_enum FROM advisory_status s WHERE a.status_id = s.id;`
  Then `ALTER TABLE advisory ALTER COLUMN status SET NOT NULL;` — if any advisory had a NULL/dangling `status_id`, this step fails and the whole migration rolls back. Do not default missing values to `New`.
- Use `extension::postgres::Type::create().as_enum(...).values([...])` from `sea_orm_migration` to create the type and `Type::drop()` in `down`.
- Down migration: recreate `advisory_status`, insert the four rows with their original IDs (read them from `m0001_initial`), add `advisory.status_id`, backfill via `UPDATE advisory a SET status_id = s.id FROM advisory_status s WHERE s.<name_col> = a.status::text`, set NOT NULL, recreate the FK, drop `advisory.status`, drop `advisory_status_enum`.
- Zero-downtime: this migration removes a column read by the currently deployed code. It must ship in the same release as Tasks 3–5 (enforced by the feature branch). Note the lock impact of `ALTER TABLE` + backfill on large tables; the Feature requires validation against a production-sized dataset before deployment.
- Per CONVENTIONS.md §Framework: use SeaORM migration APIs (`sea_orm_migration::prelude`) rather than raw ad-hoc SQL scripts, falling back to `manager.get_connection().execute_unprepared` only for the backfill `UPDATE`. Applies: task modifies migration/src/m0002_advisory_status_enum/mod.rs matching the convention's SeaORM `.rs` database code scope. Example: `migration/src/m0001_initial/mod.rs`.
- Per CONVENTIONS.md §Testing: add migration integration tests that run against the real PostgreSQL test database used by `tests/api/`. Applies: task modifies migration/src/m0002_advisory_status_enum/mod.rs matching the convention's Rust test-against-real-PostgreSQL scope. Example: `tests/api/advisory.rs`.
- Constraints (docs/constraints.md): §1.4 keep changes scoped to the task; §2.1–2.3 commits reference TC-9005 task key in the footer, use Conventional Commits, include an `Assisted-by:` trailer; §3.3/§3.4 open the PR with `--base TC-9005`; §5.1 only touch the files listed; §5.2 inspect `m0001_initial` before writing the migration; §5.4 reuse existing migration patterns.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs::Migration` — existing migration showing the project's `MigrationTrait` structure and the original `advisory_status` table / `advisory.status_id` FK definitions to reverse in `down`
- `migration/src/lib.rs::Migrator` — migration registration list to extend

## Acceptance Criteria
- [ ] `advisory_status_enum` type exists with exactly the values `New`, `Analyzing`, `Fixed`, `Rejected` after `up`
- [ ] `advisory.status` exists, is `NOT NULL`, and every pre-existing advisory row has the status matching its former `status_id` join
- [ ] `advisory.status_id` column and its FK constraint no longer exist after `up`
- [ ] `advisory_status` table no longer exists after `up`
- [ ] Migration fails and rolls back fully (no enum column, lookup table and `status_id` still present) when any advisory row has a NULL or unmappable `status_id` — it never leaves NULL statuses or a partially applied schema
- [ ] `down` restores the `advisory_status` table with its four rows, `advisory.status_id` with correct values and FK, and removes `advisory.status` and `advisory_status_enum`
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Test: seed advisories with each of the four statuses under the old schema, run `up`, assert each `advisory.status` matches the original status and the lookup table/`status_id` are gone
- [ ] Test: run `up` then `down`, assert schema and data equal the pre-migration state (round-trip)
- [ ] Test (fail-closed): seed an advisory with a dangling/NULL `status_id`, run `up`, assert the migration returns an error and the schema is unchanged (lookup table present, no `status` column, no enum type)
- [ ] Test: re-running the migrator after a successful `up` is a no-op

## Verification Commands
- `cargo test -p migration` — all migration tests pass
- `cargo run -p migration -- up && cargo run -p migration -- down` — both complete without error against a test database

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
