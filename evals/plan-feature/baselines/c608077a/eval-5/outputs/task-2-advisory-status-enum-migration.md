# Task 2 — Add migration converting advisory_status lookup table to advisory_status_enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Add a single, reversible, atomic database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. This is the schema foundation for feature TC-9005: it eliminates the `advisory_status` join from advisory queries (target: ~40ms reduction in advisory list p95 latency).

The migration must, in order and inside one transaction:
1. Create the PostgreSQL enum type `advisory_status_enum` with values `New`, `Analyzing`, `Fixed`, `Rejected`.
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table.
3. Backfill `advisory.status` from the existing `advisory.status_id` → `advisory_status(id)` join.
4. Set `advisory.status` to `NOT NULL` once the backfill is verified complete.
5. Drop the `status_id` foreign key constraint and column from `advisory`.
6. Drop the `advisory_status` lookup table.

The `down` migration must restore the previous schema (recreate `advisory_status`, re-seed its four rows, re-add `advisory.status_id` with its FK, backfill from `advisory.status`, drop `advisory.status` and the enum type).

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the `Migrator` migrations list, after `m0001_initial`

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — new SeaORM migration implementing the enum creation, column add + backfill, FK/column drop, and lookup table drop (with full `down` reversal)

## Implementation Notes
- Follow the structure of the existing migration in `migration/src/m0001_initial/mod.rs` (SeaORM `MigrationTrait` with `up`/`down`, `DeriveMigrationName`) and the registration pattern in `migration/src/lib.rs`. Name the module with the next sequential prefix (`m0002_...`) matching the `m0001_initial` naming scheme.
- Do NOT edit `migration/src/m0001_initial/mod.rs` to remove the original `advisory_status` creation — already-applied migrations must stay immutable. The Feature goal "remove the `advisory_status` table and its migration history" is satisfied by dropping the table in this forward migration; rewriting applied migration history would break existing deployments.
- Atomicity (NFR): all six steps must run inside one transaction so that a failure at any step rolls back the whole migration. PostgreSQL supports transactional DDL including `CREATE TYPE`, `ALTER TABLE`, and `DROP TABLE`; do not split the work across multiple migrations and do not use statements that cannot run in a transaction (e.g., `ALTER TYPE ... ADD VALUE`, `CREATE INDEX CONCURRENTLY`). Use the SeaORM `SchemaManager` with the connection's transaction, or wrap raw SQL via `manager.get_connection().execute_unprepared(...)` inside the migration.
- Backfill: use a single `UPDATE advisory a SET status = s.name::advisory_status_enum FROM advisory_status s WHERE a.status_id = s.id`. Verify the lookup table's name column values match the enum labels exactly (`New`, `Analyzing`, `Fixed`, `Rejected`); if the stored values differ in case, map explicitly with a `CASE` expression.
- Fail-closed backfill guard: before setting `NOT NULL` and dropping `status_id`, check that no `advisory` row has a non-null `status_id` with a null `status` (i.e., an unmapped lookup value). If any exist, raise an error so the transaction rolls back — never drop `status_id` while leaving rows with a silently-null status.
- Zero downtime (NFR): the migration takes `ACCESS EXCLUSIVE` locks on `advisory`; keep the transaction short (single `UPDATE` backfill, no per-row loops). Because the old code and the new code are incompatible with each other's schema, the migration and the code from Tasks 3–5 must be deployed together (enforced by the feature-branch workflow). Note in the PR that the migration must be tested against a production-sized dataset before deployment (Customer Considerations).
- Consider adding an index on `advisory.status` since UC-1 filters `WHERE status = 'Fixed'` on the advisory list endpoint.
- Per CONVENTIONS.md §Framework: use SeaORM (migration crate `sea-orm-migration`) APIs for schema changes rather than an external migration tool. Applies: task modifies migration/src/m0002_advisory_status_enum/mod.rs matching the convention's SeaORM database `.rs` scope. See `migration/src/m0001_initial/mod.rs` for the established pattern.
- Constraints (docs/constraints.md): commits must reference the Jira task ID in the footer (§2.1), follow Conventional Commits (§2.2), and include an `Assisted-by:` trailer (§2.3); the PR must be opened with `--base TC-9005` matching this task's Target Branch (§3.3) and its link posted to the Jira task (§3.2); changes must be scoped to the files listed above (§5.1), inspected before modification (§5.2), and must not duplicate existing functionality (§5.4).

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration that defines the `advisory` and `advisory_status` tables; reference it for table/column identifiers (`Iden` enums) and the `up`/`down` structure to mirror in the new migration
- `migration/src/lib.rs::Migrator` — migration registry where the new module must be appended

## Acceptance Criteria
- [ ] PostgreSQL enum type `advisory_status_enum` exists with exactly the values `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] `advisory.status` column of type `advisory_status_enum` exists, is `NOT NULL`, and every pre-existing advisory row carries the status previously referenced by its `status_id`
- [ ] `advisory.status_id` column and its foreign key constraint are dropped
- [ ] `advisory_status` table is dropped
- [ ] The migration runs in a single transaction: a failure at any step leaves the schema unchanged (no partial state where the enum column exists but the lookup table is dropped, or vice versa)
- [ ] The migration fails (and rolls back) rather than proceeding when any advisory row has a `status_id` that cannot be mapped to an enum value
- [ ] The `down` migration restores the `advisory_status` table, its four rows, and `advisory.status_id` with correct values, and drops `advisory.status` and `advisory_status_enum`
- [ ] `migration/src/m0001_initial/mod.rs` is unchanged

## Test Requirements
- [ ] Migration up test: seed `advisory_status` and advisories with each of the four statuses, run the migration, assert each advisory's `status` matches its original lookup value and that `advisory_status` / `status_id` no longer exist
- [ ] Migration down test (round trip): run up then down, assert the original schema and `status_id` values are restored
- [ ] Failure/rollback test: seed an advisory whose `status_id` references a lookup row with a value not in the enum, run the migration, assert it errors and the schema (including `advisory_status` and `status_id`) is unchanged
- [ ] Run against an empty `advisory` table to confirm the migration succeeds with no rows

## Verification Commands
- `cargo test -p migration` — all migration tests pass
- `cargo build --workspace` — workspace compiles (note: dependent code is updated in Tasks 3–5 on the same feature branch)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
