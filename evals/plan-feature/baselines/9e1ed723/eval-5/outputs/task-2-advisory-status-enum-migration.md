**Summary:** Add reversible migration replacing advisory_status table with advisory_status_enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Add a new SeaORM migration that moves advisory lifecycle status from the `advisory_status` lookup table, referenced by `advisory.status_id`, to a PostgreSQL enum column `advisory.status`. The join on every advisory query goes away, which should cut about 40ms from the advisory list endpoint's p95 (TC-9005).

The migration must run as a single atomic, reversible unit:
1. Create enum type `advisory_status_enum` with values `New`, `Analyzing`, `Fixed`, `Rejected`.
2. Add column `advisory.status advisory_status_enum`.
3. Backfill `advisory.status` from the existing `advisory.status_id` → `advisory_status` join.
4. Set `advisory.status` to `NOT NULL` once the backfill succeeds.
5. Drop the FK constraint and the `advisory.status_id` column.
6. Drop the `advisory_status` table.

`down()` must reverse every step: recreate `advisory_status` and seed its four rows, re-add `status_id` with its FK, backfill it from `status`, drop `status`, then drop the enum type.

## Files to Modify
- `migration/src/lib.rs` — register the new migration in the `Migrator` migrations list, after `m0001_initial`

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — new migration implementing `up()` and `down()` as described above

## Implementation Notes
- Follow the structure of the existing migration `migration/src/m0001_initial/mod.rs`: the `MigrationTrait` impl with `up`/`down`, and the `DeriveMigrationName` naming. Name the directory and module consistently with `m0001_initial` (`m0002_<description>`).
- **Atomicity (NFR):** the whole `up()` (and `down()`) must run inside one transaction. PostgreSQL supports transactional DDL. Run the steps through the migration's `SchemaManager` connection in a single transaction (or rely on the migrator's per-migration transaction if `migration/src/lib.rs` already enables it; check this). If any step fails (for example, the backfill finds an `advisory_status` value outside the four enum values), the migration must roll back completely. A state where the enum column exists but the lookup table is gone, or the reverse, must be impossible.
- **Fail-closed backfill:** do not silently default unmapped or NULL `status_id` rows to `New`. After the backfill `UPDATE`, setting `status` to `NOT NULL` is the guard: if any row is left NULL, the `ALTER` fails and the transaction rolls back. If the current schema allows NULL `status_id`, raise the default with the stakeholder rather than guessing.
- Enum creation: use `Type::create().as_enum(...)` from `sea_orm_migration::prelude::extension::postgres` (or raw `CREATE TYPE ... AS ENUM` via `execute_unprepared`). Keep the values exactly `New`, `Analyzing`, `Fixed`, `Rejected` so they match the strings the API returns today. The response shape must not change.
- Backfill SQL pattern: `UPDATE advisory a SET status = s.name::advisory_status_enum FROM advisory_status s WHERE a.status_id = s.id;`. Check the actual column name of the label in `advisory_status` (as defined in `m0001_initial`) before writing this.
- Do **not** edit `migration/src/m0001_initial/mod.rs`. Databases that already applied it must keep working. The table is dropped by this forward migration (see the impact map clarification about "migration history").
- **Zero downtime:** `ADD COLUMN` without a default and an `UPDATE` backfill take locks on `advisory`. Keep the migration to one pass and avoid per-row loops.
- Per CONVENTIONS.md §Framework: use SeaORM (`sea_orm_migration`) for all schema operations.
  Applies: task modifies `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's `.rs` SeaORM/database file scope.
- Per CONVENTIONS.md §Error handling: return errors from `up()`/`down()` (`Result<(), DbErr>`) rather than panicking, so the migrator can roll back.
  Applies: task modifies `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's `.rs` Rust source scope.
- Constraints (docs/constraints.md): §2 commits must use Conventional Commits, include the `Implements TC-<task>` footer and an `Assisted-by:` trailer. §3 the PR must use `--base TC-9005` and the PR link must be posted to the Jira task. §5 changes stay scoped to the listed files, inspect code before modifying it, and follow the patterns referenced here.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration that created `advisory_status` and `advisory.status_id`. Use it as the structural template and as the source of the exact table and column names for the backfill and the `down()` recreation.
- `migration/src/lib.rs::Migrator` — existing migrator registration list to extend

## Acceptance Criteria
- [ ] `migration/src/m0002_advisory_status_enum/mod.rs` exists and is registered in `migration/src/lib.rs`
- [ ] After `up()`, the PostgreSQL type `advisory_status_enum` exists with exactly the values `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] After `up()`, `advisory.status` exists, is `NOT NULL`, and every pre-existing row's value equals the name its old `status_id` pointed to
- [ ] After `up()`, `advisory.status_id` and the `advisory_status` table no longer exist
- [ ] `down()` restores the original schema (`advisory_status` table with its four rows, `advisory.status_id` FK populated from `status`) and drops `advisory_status_enum`
- [ ] Migration is atomic: if any step fails (e.g., a row cannot be mapped), no partial schema change remains. The enum column and the lookup table never coexist in a half-migrated state, and the lookup table is never dropped without the column existing
- [ ] Rows with an unmappable or NULL status make the migration fail and roll back. They are not silently defaulted

## Test Requirements
- [ ] Migration test: seed advisories with each of the four statuses through the old schema, run `up()`, and assert every row's `status` matches the original status name
- [ ] Migration test: assert `advisory_status` and `advisory.status_id` are absent after `up()`
- [ ] Reversibility test: run `up()` then `down()` and assert the original schema and data are restored (statuses preserved round-trip)
- [ ] Atomicity / fail-closed test: seed an advisory whose status cannot be mapped (or whose `status_id` is NULL), run `up()`, and assert it returns an error **and** the schema is unchanged (`advisory_status` still exists, `advisory.status` does not)
- [ ] Performance check (pre-deployment, per Customer Considerations): run the migration against a production-sized dataset and record the duration and lock impact

## Verification Commands
- `cargo test -p migration` — all migration tests pass
- `cargo run -p migration -- up && cargo run -p migration -- down && cargo run -p migration -- up` — completes without error against a local PostgreSQL

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
