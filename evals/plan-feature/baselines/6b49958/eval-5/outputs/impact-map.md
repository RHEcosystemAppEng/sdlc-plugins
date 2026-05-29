# Repository Impact Map — TC-9005

## trustify-backend

changes:
  - Create database migration to add `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from existing `status_id` join, drop `status_id` foreign key column, and drop `advisory_status` lookup table
  - Update SeaORM entity definition in `entity/src/advisory.rs` to replace `status_id` foreign key field with `status` enum field, and remove `entity/src/advisory_status.rs`
  - Update `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` to query using the new `status` enum column instead of joining `advisory_status`
  - Update advisory model structs (`AdvisorySummary`, `AdvisoryDetails`) to source status from the enum column
  - Update advisory endpoints (`list.rs`, `get.rs`) to filter/sort by enum column instead of joined table
  - Update advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into lookup table
  - Update advisory integration tests in `tests/api/advisory.rs` to reflect new schema and query patterns
  - Update `entity/src/lib.rs` to remove `advisory_status` module export

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migrations** — The migration drops the `advisory_status` table and `status_id` column while adding a new `status` enum column. Merging the migration without the code changes would break all advisory queries (they still reference `status_id` and join `advisory_status`). Merging the code changes without the migration would reference a `status` column that does not exist.
2. **Breaking API changes** — The service layer and endpoints switch from joining `advisory_status` to querying `advisory.status` directly. The entity definitions change from a foreign key relationship to an enum field. These are tightly coupled: the old entity/service code cannot function with the new schema, and the new entity/service code cannot function with the old schema.
3. **Tightly coupled feature components** — The ingestion pipeline, service layer, entity definitions, and migration are all interdependent. Each component references data structures that change across the feature.

The feature's non-functional requirements explicitly state: "All changes must land together: merging the migration without the code changes would break all advisory queries."

**Interdependent tasks:** All intermediate tasks (migration, entity update, service update, endpoint update, ingestion update, test update) depend on each other because partial delivery would leave the codebase in an inconsistent state.

**Label:** Apply `workflow:feature-branch` to feature issue TC-9005.
