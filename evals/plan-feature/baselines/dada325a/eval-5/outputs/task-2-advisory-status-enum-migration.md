**Summary:** Add reversible migration converting advisory_status lookup table to advisory_status_enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Add a new SeaORM migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on `advisory`. In a single transaction, the migration must:

1. Create the enum type `advisory_status_enum` with the values `New`, `Analyzing`, `Fixed`, `Rejected`.
2. Add a `status` column of type `advisory_status_enum` to `advisory`.
3. Backfill `advisory.status` from the existing `advisory.status_id` → `advisory_status(id)` join.
4. Set `advisory.status` to `NOT NULL` once the backfill is done.
5. Drop the `advisory.status_id` foreign key constraint and column.
6. Drop the `advisory_status` lookup table.

The migration must be fully reversible. `down()` recreates `advisory_status` and reseeds its four rows. It re-adds `status_id` with its FK and backfills it from `status`. Then it drops the `status` column and the `advisory_status_enum` type.

This is the schema half of TC-9005. Tasks 3–5 (entity, queries, ingestion) depend on it, and all of them land together through the `TC-9005` feature branch.

## Files to Modify
- `migration/src/lib.rs` — register the new migration in the `Migrator`'s migration list, after `m0001_initial`

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — new migration implementing `up()` (enum creation, column add, backfill, drop FK/column, drop table) and `down()` (full reversal)

## Implementation Notes
- Follow the module layout of the existing migration `migration/src/m0001_initial/mod.rs`: one directory per migration with a `mod.rs` that implements `MigrationTrait` (`up` / `down`). Register it in `migration/src/lib.rs` the same way `m0001_initial` is registered. Use the next sequential prefix (`m0002_…`). If other migrations exist beyond what the repository listing shows, use the next free number.
- **Atomicity (NFR):** run every step of `up()` in one transaction, and do the same for `down()`. PostgreSQL DDL is transactional, so `CREATE TYPE`, `ALTER TABLE … ADD COLUMN`, `UPDATE … FROM advisory_status`, `ALTER TABLE … DROP COLUMN` and `DROP TABLE` can share a single transaction. Use `manager.get_connection().begin()` or make sure the migrator's per-migration transaction covers every statement. Do not commit between steps, because a partial state (enum column present but lookup table dropped, or the reverse) is explicitly forbidden.
- **Fail-closed backfill:** the backfill must not quietly leave `status` as `NULL` for rows whose `status_id` is `NULL` or points at a name outside the four enum values. Before dropping `status_id`, run a guard query: `SELECT count(*) FROM advisory WHERE status IS NULL`. If the count is non-zero, return a `DbErr` so the whole migration rolls back. The final `ALTER COLUMN status SET NOT NULL` is a second safety net. Cast with an explicit mapping, e.g. `UPDATE advisory a SET status = s.name::advisory_status_enum FROM advisory_status s WHERE a.status_id = s.id`. A cast failure on an unexpected name must also abort the transaction.
- **Zero downtime (NFR):** use `ALTER TABLE … ADD COLUMN` with no default plus an `UPDATE` backfill, then `SET NOT NULL`. This avoids a table rewrite on add. The `UPDATE` and `SET NOT NULL` still take locks on `advisory`. Record the lock duration from the production-sized dataset test (see Test Requirements) in the PR description. Running application code still reads `status_id` until the code changes from Tasks 3–5 are deployed, so the migration and the code must be deployed together from the merged feature branch.
- Do **not** edit `migration/src/m0001_initial/mod.rs`. The feature goal "Remove the `advisory_status` table and its migration history" is met by the new forward migration. Rewriting the initial migration would break databases that have already applied it (see impact map, clarification item).
- Use SeaORM migration builders (`Type::create()`, `Table::alter()`, `Table::drop()`, `ForeignKey::drop()`) where they exist. Use `manager.get_connection().execute_unprepared(...)` for the enum cast backfill and the guard query, which need raw SQL.
- Constraints (docs/constraints.md):
  - §2.1–2.3: commits must reference TC-9005's task key in the footer (`Implements <task-key>`), follow Conventional Commits (e.g., `feat(migration): …`), and carry an `Assisted-by:` trailer.
  - §3.3/§3.4: open the PR with `gh pr create --base TC-9005`.
  - §5.1–5.4: keep changes to the files listed here, inspect `m0001_initial` before writing, and reuse the existing migration patterns.
  - §1.4: no unrelated refactoring.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing `MigrationTrait` implementation. It is the pattern for structure, `Iden` enums for table and column names, and how the `advisory` and `advisory_status` tables were first defined. Copy the `advisory_status` definition from it into `down()`.
- `migration/src/lib.rs::Migrator` — migration registration list to extend.

## Acceptance Criteria
- [ ] PostgreSQL enum type `advisory_status_enum` exists with exactly the values `New`, `Analyzing`, `Fixed`, `Rejected` after `up()`
- [ ] `advisory.status` column exists, is of type `advisory_status_enum`, and is `NOT NULL`
- [ ] Every pre-existing advisory row has `status` equal to the name of the `advisory_status` row its `status_id` referenced
- [ ] `advisory.status_id` column and its foreign key constraint no longer exist
- [ ] `advisory_status` table no longer exists
- [ ] The migration fails closed: if any advisory row would end up with a `NULL` or unmappable status, `up()` returns an error and the database is left exactly as before the migration (no enum type, no `status` column, `status_id` and `advisory_status` intact)
- [ ] `up()` and `down()` each run in a single transaction. A failure at any step rolls back all prior steps
- [ ] `down()` restores the original schema (`advisory_status` table with its four rows, `advisory.status_id` FK populated from `status`) and drops `status` and `advisory_status_enum`
- [ ] The migration is registered in `migration/src/lib.rs` and runs as part of the standard migrator

## Test Requirements
- [ ] Migration test: seed `advisory_status` with the four statuses and advisories that reference each one. Run `up()`, then assert each advisory's `status` matches its original status name and that `status_id` and `advisory_status` are gone
- [ ] Reversibility test: run `up()` then `down()`, then assert the original schema and data are restored (same `status_id` → status name mapping per advisory)
- [ ] Fail-closed test: seed an advisory with `status_id = NULL` (or a status name outside the enum). Run `up()` and assert it returns an error **and** that the schema is unchanged: `advisory_status` still exists, `status_id` still exists, there is no `status` column, and there is no `advisory_status_enum` type. This proves the transaction rolled back and did not partially apply
- [ ] Empty table test: `up()` succeeds on an empty `advisory` table
- [ ] Run the migration against a production-sized dataset before deployment (Customer Considerations) and record its duration and lock time in the PR description

## Verification Commands
- `cargo test -p migration` — all migration tests pass
- `psql -c "\dT+ advisory_status_enum"` (after running migrations on a test DB) — shows the four enum values
- `psql -c "\d advisory"` — shows a `status` column of type `advisory_status_enum` and no `status_id`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
