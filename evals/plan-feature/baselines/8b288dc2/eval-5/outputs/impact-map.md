# Repository Impact Map

## Feature: TC-9005 — Drop status table and migrate to enum column

### trustify-backend:
  changes:
    - Create PostgreSQL enum type `advisory_status_enum` and add `status` enum column to `advisory` table with backfill from existing `status_id` join
    - Drop `status_id` foreign key column and `advisory_status` lookup table after backfill
    - Update SeaORM entity definitions: modify `entity/advisory.rs` to use enum column, remove `entity/advisory_status.rs`
    - Update `AdvisoryService` queries to use direct enum column instead of join through `advisory_status` table
    - Update advisory ingestion pipeline to write enum values directly instead of inserting into lookup table
    - Update advisory endpoints and integration tests to reflect new schema

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators are present:

1. **Coordinated schema migrations** — the migration adds the `advisory_status_enum` type and `status` column while simultaneously dropping `status_id` and the `advisory_status` table. All code that queries advisories must be updated in the same deployment; partial delivery would leave queries referencing a dropped table or missing column.

2. **Breaking API changes** — dropping the `advisory_status` table breaks every advisory query that joins on it. The service layer, endpoints, and ingestion pipeline all depend on the current schema; merging the migration without the code changes would cause runtime failures.

3. **Tightly coupled feature components** — the feature's NFRs explicitly state "All changes must land together: merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist."

**Interdependent tasks:** All intermediate tasks (migration, entity updates, service updates, ingestion updates, endpoint updates) are structurally interdependent — each depends on the schema change introduced by the migration task and cannot function independently on `main`.

**Label:** `workflow:feature-branch` will be applied to the feature issue.
