**Summary:** Add migration replacing advisory_status table with advisory_status_enum column
**Epic:** TC-9005: Advisory status schema migration

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Add a single, reversible, atomic SeaORM migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on `advisory`. In order, within one transaction, the migration must:

1. Create enum type `advisory_status_enum` with values `New`, `Analyzing`, `Fixed`, `Rejected`.
2. Add column `advisory.status advisory_status_enum` (nullable initially).
3. Backfill `advisory.status` from the existing `advisory.status_id` → `advisory_status` join.
4. Set `advisory.status` to `NOT NULL` once backfill is verified complete.
5. Drop the `advisory.status_id` foreign key constraint and column.
6. Drop the `advisory_status` table.

`down()` must reverse all steps (recreate `advisory_status` with its four rows, re-add `status_id`, backfill it from `status`, restore the FK, drop `status`, drop the enum type). This removes the join overhead on every advisory query (Feature TC-9005).

## Files to Modify
- `migration/src/lib.rs` — register the new migration in the `Migrator` migrations list after `m0001_initial`

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — the enum migration (`up` / `down`)

## Implementation Notes
- Follow the migration structure in `migration/src/m0001_initial/mod.rs` (the `MigrationTrait` impl and `DeriveMigrationName`). Read it to obtain the exact `advisory_status` table definition (column names, the id values for New/Analyzing/Fixed/Rejected) needed by both the backfill join and `down()`.
- Atomicity: PostgreSQL supports transactional DDL. Ensure all steps run inside one transaction (SeaORM runs each migration in a transaction on Postgres; do not split the steps across multiple migrations and do not call anything that commits mid-migration). `CREATE TYPE` and `ALTER TABLE` are transactional on Postgres; `ALTER TYPE ... ADD VALUE` is not — do not use it.
- Use `manager.get_connection().execute_unprepared(...)` for `CREATE TYPE advisory_status_enum AS ENUM (...)` and the backfill `UPDATE advisory a SET status = s.name::advisory_status_enum FROM advisory_status s WHERE a.status_id = s.id`, and `manager.alter_table` / `manager.drop_table` (SeaQuery) for column and table drops, matching the style of `m0001_initial`.
- **Fail-closed backfill:** after the `UPDATE`, check `SELECT count(*) FROM advisory WHERE status IS NULL`. If non-zero (a `status_id` was NULL or referenced a row whose name is not one of the four enum values), return a `DbErr` so the whole migration rolls back. Do not default unmapped rows to `New` and do not proceed to drop `status_id` / `advisory_status`. The `SET NOT NULL` in step 4 is the second guard.
- Zero-downtime: avoid long-held locks — no table rewrite beyond the single `UPDATE`; add the column without a volatile default. Flag in the PR description that dropping `status_id` / `advisory_status` breaks any still-running pre-TC-9005 binary, so migration and binary rollout must be coordinated.
- Constraints to honor (docs/constraints.md): §2 commits reference the Jira task ID, use Conventional Commits, include an `Assisted-by:` trailer; §3 PR uses `--base TC-9005` and the PR link is posted to the Jira task; §5 changes are limited to the files listed here, inspect code before modifying, no duplicated functionality.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern and the original `advisory_status` / `advisory.status_id` definitions to mirror in `down()`

## Acceptance Criteria
- [ ] Enum type `advisory_status_enum` exists with exactly the values `New`, `Analyzing`, `Fixed`, `Rejected` after `up()`
- [ ] `advisory.status` exists, is `NOT NULL`, and every pre-existing row holds the status previously resolved via `status_id`
- [ ] `advisory.status_id` column and its FK no longer exist after `up()`
- [ ] `advisory_status` table no longer exists after `up()`
- [ ] If any advisory row cannot be mapped to an enum value, `up()` returns an error and the database is left exactly as before (no enum type, no `status` column, `status_id` and `advisory_status` intact)
- [ ] A failure in any step rolls back the entire migration (no partial state)
- [ ] `down()` restores `advisory_status` (four rows), `advisory.status_id` with FK and original values, and removes `advisory.status` and `advisory_status_enum`
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration test: seed advisories with each of the four statuses under the old schema, run `up()`, assert `advisory.status` matches the original status for every row and `advisory_status` / `status_id` are gone
- [ ] Migration test: run `up()` then `down()`, assert schema and data are restored to the pre-migration state (round-trip)
- [ ] Fail-closed test: seed an advisory whose `status_id` is NULL or points at a non-enum status name, run `up()`, assert it returns an error and that `advisory_status`, `advisory.status_id` still exist and `advisory.status` / `advisory_status_enum` do not
- [ ] Run the migration against a production-sized dataset (staging snapshot) and record duration and lock behavior before deployment (Feature: Customer Considerations)

## Verification Commands
- `cargo build -p migration` — compiles
- `cargo test -p migration` — migration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
