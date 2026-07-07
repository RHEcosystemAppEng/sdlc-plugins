# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migrations** — The database migration creates an enum type, adds a column, backfills data, drops the foreign key column, and drops the lookup table. The code changes (entity definitions, service queries, ingestion pipeline) depend on these schema changes being present. Merging the migration without the code changes would leave queries joining a dropped table; merging the code changes without the migration would reference a non-existent column.

2. **Breaking API changes** — The service layer and endpoints currently join the `advisory_status` table via `status_id`. After the migration drops this table, all advisory queries must use the new `status` enum column. These changes are mutually dependent — neither side functions without the other.

3. **Tightly coupled feature components** — The feature's non-functional requirements explicitly state: "All changes must land together: merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist."

**Interdependent tasks:** All implementation tasks (migration, entity updates, service/endpoint updates, ingestion pipeline updates, integration tests) are structurally interdependent — partial delivery would leave the codebase in an inconsistent state.

The `workflow:feature-branch` label will be applied to the feature issue TC-9005.

---

## trustify-backend

### Changes

- Create a reversible database migration that: defines the `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected); adds a `status` enum column to the `advisory` table; backfills the `status` column from the existing `advisory_status` join; drops the `status_id` foreign key column; drops the `advisory_status` lookup table
- Update SeaORM entity definition in `entity/src/advisory.rs` to replace `status_id` foreign key field with a `status` enum field mapped to `advisory_status_enum`
- Remove the `entity/src/advisory_status.rs` entity file and its module registration in `entity/src/lib.rs`
- Update `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` to query the `status` enum column directly instead of joining the `advisory_status` table
- Update `AdvisorySummary` and `AdvisoryDetails` model structs to source status from the enum column
- Update advisory list and get endpoints in `modules/fundamental/src/advisory/endpoints/` to use the new status field for filtering
- Update advisory ingestion in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into the lookup table
- Update advisory integration tests in `tests/api/advisory.rs` for the new schema
- Update internal architecture documentation to reflect the schema change

---

## Excluded Requirements

None. All requirements from the Feature description can be decomposed into actionable tasks within the trustify-backend repository.
