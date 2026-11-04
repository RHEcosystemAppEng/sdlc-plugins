## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Add a single, reversible, atomic SeaORM migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. In one migration the implementer must:

1. Create the PostgreSQL enum type `advisory_status_enum` with values `New`, `Analyzing`, `Fixed`, `Rejected`.
2. Add a `status` column of type `advisory_status_enum` to `advisory`.
3. Backfill `advisory.status` from the existing `advisory.status_id` -> `advisory_status(id)` join.
4. Make `advisory.status` `NOT NULL` after the backfill.
5. Drop the `advisory.status_id` foreign key constraint and column.
6. Drop the `advisory_status` lookup table.

The `down()` migration must restore the previous schema: recreate `advisory_status` with its four rows, re-add `advisory.status_id` with its FK, backfill it from `advisory.status`, then drop the `status` column and the `advisory_status_enum` type.

This is part of TC-9005. It provides the schema the entity, query, and ingestion tasks depend on.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the `Migrator` migrations list, after `m0001_initial`

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — new migration that creates the enum type, adds and backfills `advisory.status`, drops `advisory.status_id` and the `advisory_status` table, plus the reverse `down()` path

## Implementation Notes
- Follow the existing migration module layout in `migration/src/m0001_initial/mod.rs`: one directory per migration with a `mod.rs` that implements `MigrationTrait` (`up` / `down`), registered in `migration/src/lib.rs`.
- Per CONVENTIONS.md §Framework: use SeaORM (`sea_orm_migration`) for all schema changes. Use `Type::create().as_enum(...)` / `extension::postgres::Type` for the enum type and `Table::alter()` for column changes. Fall back to `manager.get_connection().execute_unprepared(...)` only for the backfill `UPDATE ... FROM advisory_status` statement, which has no clean builder form.
  Applies: task modifies migration/src/m0002_advisory_status_enum/mod.rs matching the convention's SeaORM `.rs` database code scope.
- **Atomicity (NFR):** all six steps must execute inside one migration so they share one transaction. SeaORM runs each migration in a transaction on PostgreSQL; do NOT split the steps across several migration files, because a failure between files would leave the enum column present while the lookup table is already gone (or the reverse).
- **Fail-closed backfill (fail-open risk):** a backfill that skips rows quietly would still "succeed" and leave `status` `NULL` or defaulted. Guard it in `up()` in `migration/src/m0002_advisory_status_enum/mod.rs`:
  - Do not give the new column a `DEFAULT` value during backfill.
  - Before dropping `status_id`, run a check query (`SELECT count(*) FROM advisory WHERE status IS NULL`). If any rows remain unmapped (a `status_id` pointing at a name outside the four enum values, or a `NULL` `status_id`), return an `Err(DbErr::Migration(...))` so the transaction rolls back. Never coerce those rows to `New`.
  - The `ALTER COLUMN status SET NOT NULL` step acts as a second database-level guard.
- Map the backfill by name rather than by numeric id (`UPDATE advisory a SET status = s.name::advisory_status_enum FROM advisory_status s WHERE a.status_id = s.id`), so it does not depend on the id assignment in `m0001_initial`.
- Zero-downtime caveat: dropping `status_id` and `advisory_status` breaks any application instance still running the pre-TC-9005 code. Deployment has to roll the new binary and the migration together, which is why this feature uses feature-branch mode. Record this in the PR description.
- Do NOT edit `migration/src/m0001_initial/mod.rs`. Migrations that have already been applied are immutable. The feature's "remove migration history" goal is met by dropping the table in this forward migration (see the impact map's open questions).
- Constraints (docs/constraints.md): commits follow Conventional Commits and reference TC-9005 in the footer with the `Assisted-by: Claude Code` trailer (§2.1–2.3). Open the PR with `--base TC-9005` (§3.3). Keep changes scoped to the listed files (§5.1) and inspect existing code before modifying it (§5.2).

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration showing the `MigrationTrait` structure and the original `advisory` / `advisory_status` table definitions (column names, FK name) needed for an exact `down()` restore
- `migration/src/lib.rs::Migrator` — migration registry to extend

## Acceptance Criteria
- [ ] PostgreSQL enum type `advisory_status_enum` exists with exactly the values `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] `advisory.status` exists, is `NOT NULL`, and is of type `advisory_status_enum`
- [ ] Every existing advisory's `status` matches the name of the `advisory_status` row its old `status_id` referenced
- [ ] `advisory.status_id` and its FK constraint are dropped
- [ ] The `advisory_status` table is dropped
- [ ] The migration fails and rolls back fully (no enum type, no `status` column, `status_id` and `advisory_status` intact) when any advisory row cannot be mapped to an enum value. It never silently defaults or nulls such rows.
- [ ] `down()` restores the original schema and data (`advisory_status` rows, `advisory.status_id` FK values)
- [ ] The migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration test: seed advisories with each of the four statuses on the pre-migration schema, run `up()`, and assert that each row's `status` equals its original status name and that `advisory_status` / `status_id` no longer exist
- [ ] Fail-closed test: seed an advisory whose `status_id` references a status name outside the enum (or has a `NULL` `status_id`), run `up()`, and assert it returns an error and that the schema is unchanged (the `advisory_status` table and `status_id` column still exist, and there is no `status` column or `advisory_status_enum` type)
- [ ] Round-trip test: run `up()` then `down()` and assert that the original `status_id` values and `advisory_status` rows are restored
- [ ] Run the migration against a production-sized dataset before deployment (Customer Considerations). Record timing in the PR.

## Verification Commands
- `cargo build --manifest-path migration/Cargo.toml` — compiles without errors
- `cargo test --manifest-path migration/Cargo.toml` — migration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
