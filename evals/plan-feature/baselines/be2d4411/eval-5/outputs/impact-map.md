# Repository Impact Map — TC-9005

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migrations** — The migration adds a `status` enum column, backfills data from the `advisory_status` join table, drops the `status_id` FK column, and drops the `advisory_status` table. All code that references the old `status_id` FK or the `advisory_status` table must be updated before the migration runs; conversely, the new `status` enum column does not exist until the migration runs. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped table). Merging the code changes without the migration would reference a column that does not exist.

2. **Breaking API changes** — The SeaORM entity layer, advisory service, advisory endpoints, and ingestion pipeline all depend on the schema structure. Updating any one without the others would leave the codebase in an inconsistent state.

3. **Tightly coupled feature components** — The feature's Non-Functional Requirements explicitly state: "All changes must land together." The migration, entity, service, endpoint, and ingestion changes are interdependent.

**Interdependent tasks:** All intermediate tasks (migration, entity updates, service/model updates, endpoint updates, ingestion updates, test updates) are interdependent — each depends on the migration being present and the entity layer reflecting the new schema.

The `workflow:feature-branch` label will be applied to the feature issue.

---

## Impact Map

trustify-backend:
  changes:
    - Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected) and migration to add `status` enum column to `advisory` table, backfill from `advisory_status` join, drop `status_id` FK column, and drop `advisory_status` lookup table
    - Update SeaORM entity definitions: modify `entity/src/advisory.rs` to replace `status_id` FK with `status` enum column, remove `entity/src/advisory_status.rs` entity file, update `entity/src/lib.rs` module declarations
    - Update advisory model structs (`AdvisorySummary`, `AdvisoryDetails`) to populate status from enum column instead of join
    - Update advisory service queries to select status directly from `advisory.status` enum column, removing all `advisory_status` table joins
    - Update advisory endpoint query filtering to use enum column for status filters
    - Update advisory ingestion pipeline to write `advisory_status_enum` values directly instead of inserting into lookup table
    - Update advisory integration tests to verify status filtering and ingestion against new enum schema
