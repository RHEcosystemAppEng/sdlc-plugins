# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators are present:

1. **Coordinated schema migrations** — The migration creates an enum type, adds a column, backfills data, drops the foreign key column, and drops the lookup table. A partial migration (enum column exists but lookup table already dropped, or vice versa) leaves the database in an inconsistent state.
2. **Breaking API changes** — Merging the migration without the code changes breaks all advisory queries (they still join the now-dropped `advisory_status` table). Merging the code changes without the migration references a `status` column that does not exist.
3. **Tightly coupled feature components** — The entity definitions, service layer, endpoints, and ingestion pipeline all depend on the schema change landing atomically.

The `workflow:feature-branch` label will be applied to the feature issue TC-9005 in the task creation step.

---

## trustify-backend

changes:
  - Create reversible database migration: define `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from existing `status_id` join, drop `status_id` FK column, drop `advisory_status` lookup table
  - Update SeaORM entity definitions: modify `entity/src/advisory.rs` to replace `status_id` FK with `status` enum column mapping; remove `advisory_status` entity references from `entity/src/lib.rs`
  - Update advisory service layer and endpoints: modify `AdvisoryService` queries to use `status` column directly instead of joining `advisory_status` table; update list and get endpoint handlers
  - Update advisory ingestion pipeline: modify ingestion to write enum values directly to the `status` column instead of inserting into the lookup table
  - Update integration tests: modify advisory endpoint tests to work with enum status column and verify correct filtering behavior
  - Update internal architecture documentation to reflect schema change (documentation considerations from feature description)

## Inherited Field Values

- **Priority:** High (inherited from Feature TC-9005 — will be propagated to all created tasks)
- **Fix Versions:** RHTPA 2.0.0 (inherited from Feature TC-9005 — `fixVersion scope` defaults to "both" since no `### Jira Field Defaults` section is configured, so fixVersions are propagated to tasks)

## Excluded Requirements

None — all requirements are MVP and can be implemented within the single target repository.
