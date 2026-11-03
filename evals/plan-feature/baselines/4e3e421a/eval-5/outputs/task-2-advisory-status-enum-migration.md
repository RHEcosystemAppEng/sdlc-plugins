# Task 2 — Add migration converting advisory_status lookup table to advisory_status_enum column

**Summary:** Add migration converting advisory_status lookup table to advisory_status_enum column
**Labels:** ai-generated-jira
**Priority:** High (inherited from TC-9005)
**Fix Versions:** RHTPA 2.0.0 (inherited from TC-9005, fixVersion scope = both)

---

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Add one reversible SeaORM migration. It replaces the `advisory.status_id` foreign key to the `advisory_status` lookup table with an `advisory.status` column of a new PostgreSQL enum type, `advisory_status_enum`, which has the values `New`, `Analyzing`, `Fixed`, and `Rejected`. The migration backfills the new column from the existing join, then drops the `status_id` column and the `advisory_status` table.

This covers the TC-9005 requirements for the enum type, the `status` column with backfill, dropping `status_id`, and dropping `advisory_status`. It also covers the non-functional requirement that the migration is atomic. If any step fails, the whole migration must roll back. A partial state, such as the enum column existing after the lookup table is already dropped, would leave the database inconsistent.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the `Migrator` migration list, after `m0001_initial`

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — the migration (`up` and `down`) described below

## Implementation Notes
**Migration steps (`up`). All steps run inside one transaction:**
1. `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
2. `ALTER TABLE advisory ADD COLUMN status advisory_status_enum` (nullable at first so the backfill can run)
3. Backfill with `UPDATE advisory a SET status = s.name::advisory_status_enum FROM advisory_status s WHERE a.status_id = s.id`. Check the actual name column of `advisory_status` in `migration/src/m0001_initial/mod.rs` before writing this.
4. **Fail-closed guard (required):** after the backfill, run `SELECT count(*) FROM advisory WHERE status IS NULL`. If the count is not zero, return an error so the transaction rolls back. A non-zero count means orphaned `status_id` values, a NULL `status_id`, or a lookup name that does not cast to the enum. Do not continue to the drop steps when the backfill is incomplete. Otherwise the migration would report success after silently losing status data for some advisories.
5. `ALTER TABLE advisory ALTER COLUMN status SET NOT NULL`
6. Drop the FK constraint and the index on `status_id`, then `ALTER TABLE advisory DROP COLUMN status_id`
7. `DROP TABLE advisory_status`

**Reverse steps (`down`). Also one transaction:** recreate `advisory_status` (same columns and ids as defined in `m0001_initial`), re-seed the four status rows, add `advisory.status_id` with its FK constraint and index, backfill `status_id` from `status::text`, set it NOT NULL if `m0001_initial` defined it that way, drop `advisory.status`, then `DROP TYPE advisory_status_enum`.

**Transaction handling:** PostgreSQL supports transactional DDL, including `CREATE TYPE`, `ALTER TABLE`, and `DROP TABLE`. Use the `SchemaManager` connection inside an explicit transaction, or confirm that the SeaORM migrator in use wraps each migration in a transaction on PostgreSQL. Do not depend on behaviour that runs each statement separately.

**Existing pattern to follow:** `migration/src/m0001_initial/mod.rs` shows the `MigrationName` / `MigrationTrait` structure, the use of `SchemaManager`, and how the `advisory` and `advisory_status` tables and their FK were originally defined. Mirror its style for table and column identifiers.

**Zero-downtime caveat (flagged in the impact map):** this migration drops `status_id`. Application instances that are still running pre-TC-9005 code will fail on advisory queries once it commits. Running the migration and deploying the new binary must be coordinated. The open question is recorded in the impact map. Do not add an expand/contract split to this task unless the product owner resolves that question.

**Constraints (docs/constraints.md):**
- §2.1–2.3: commits reference TC-9005's task key in the footer, follow Conventional Commits (e.g., `feat(migration): ...`), and include `--trailer="Assisted-by: Claude Code"`.
- §3.3: open the PR with `--base TC-9005`.
- §5.1–5.4: limit changes to the files listed above, inspect `m0001_initial` before writing, and follow the existing migration pattern.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — original definitions of `advisory`, `advisory_status`, and the `status_id` FK. Needed to write an exact `down()` reversal and to find the real lookup column names.
- `migration/src/lib.rs::Migrator` — existing migration registration list to extend

## Acceptance Criteria
- [ ] PostgreSQL enum type `advisory_status_enum` exists with exactly the values `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] `advisory.status` column of type `advisory_status_enum` exists and is `NOT NULL`
- [ ] Every pre-existing advisory row has `status` equal to the `advisory_status` name it referenced through `status_id` before the migration
- [ ] `advisory.status_id` column, its FK constraint, and its index no longer exist
- [ ] `advisory_status` table no longer exists
- [ ] Fail-closed: if any advisory row has a NULL `status` after the backfill (orphan `status_id`, NULL `status_id`, or a lookup name that cannot be cast), the migration returns an error, the whole transaction rolls back, and `advisory_status`, `advisory.status_id`, and the existing data are left unchanged
- [ ] Atomic: a failure at any step leaves the schema exactly as it was before the migration (no enum type, no `status` column, lookup table intact)
- [ ] `down()` fully reverses the migration: `advisory_status` is recreated with its rows, `advisory.status_id` is restored with correct values and the FK, and `advisory.status` and `advisory_status_enum` are removed
- [ ] The migration is registered in `migration/src/lib.rs` and runs after `m0001_initial`

## Test Requirements
- [ ] Migration test: seed advisories covering all four statuses, run `up`, and assert each row's `status` matches its original lookup name, `status_id` is gone, and `advisory_status` is gone
- [ ] Fail-closed test: seed an advisory whose `status_id` cannot be resolved to an enum value (for example, a lookup row named `Unknown`, or a row with NULL `status_id`), run `up`, assert it returns an error, and assert `advisory_status` and `advisory.status_id` still exist with the original data, with no `status` column and no `advisory_status_enum` type
- [ ] Round-trip test: run `up` then `down` and assert the schema and data match the pre-migration state (same `status_id` values for every row)
- [ ] Empty-table test: `up` succeeds on a database with zero advisory rows

## Verification Commands
- `cargo test -p migration` — all migration tests pass
- `cargo run -p migration -- up` followed by `psql -c "\dT+ advisory_status_enum"` — the enum is listed with the four values
- `psql -c "\d advisory"` — shows `status advisory_status_enum not null` and no `status_id`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
