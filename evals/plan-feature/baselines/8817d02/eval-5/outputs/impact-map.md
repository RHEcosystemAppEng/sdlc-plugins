# Repository Impact Map — TC-9005

## trustify-backend

### Changes

- Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected) and add `status` enum column to `advisory` table with backfill from existing `status_id` join
- Drop `status_id` foreign key column and `advisory_status` lookup table after backfill
- Update SeaORM entity definition for `advisory` to use the new enum column; remove `advisory_status` entity
- Update `AdvisoryService` queries (fetch, list, search) to use the new `status` column instead of joining `advisory_status`
- Update `AdvisorySummary` and `AdvisoryDetails` model structs to source status from the enum column
- Update advisory ingestion pipeline to write enum values directly instead of inserting into the lookup table
- Update advisory endpoint handlers and query helpers for status filtering without join
- Update integration tests for advisory endpoints to reflect the new schema

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators are present:

1. **Coordinated schema migrations** — The database migration creates an enum type, adds a new column, backfills data, drops the old FK column, and drops the lookup table. All code changes (entity definitions, service queries, ingestion pipeline, endpoints) depend on this migration. Merging the migration alone would break all advisory queries that still JOIN the dropped `advisory_status` table. Merging the code changes alone would reference a `status` column that does not exist.

2. **Breaking API changes** — The entity layer, service layer, and ingestion pipeline are tightly coupled to the schema change. The `advisory.rs` entity must match the database schema; the `AdvisoryService` queries must reference the correct column; the ingestion pipeline must write to the correct column. No subset of these changes can be merged independently without breaking the application.

3. **Explicit atomicity requirement** — The feature's non-functional requirements state: "All changes must land together: merging the migration without the code changes would break all advisory queries, and merging the code changes without the migration would reference a column that does not exist."

**Interdependent tasks:** All intermediate tasks (migration, entity update, service/model update, ingestion update, endpoint update, test update) are interdependent — each depends on the schema migration being present and the entity definitions matching the new schema.

**Label:** `workflow:feature-branch`

sha256-md:57c0efe784cef59b96b9fcd9e091da104f67360f77bd021020127e9b24e5a960
