# Repository Impact Map

## Feature: TC-9005 — Drop status table and migrate to enum column

## Workflow Mode: feature-branch

**Rationale:** The feature requires `feature-branch` mode due to the following atomicity indicators:

1. **Coordinated schema migrations** — The database migration creates the `advisory_status_enum` type, adds the `status` column, backfills data, drops the `status_id` FK column, and drops the `advisory_status` table. The code changes (entity definitions, service layer, endpoints, ingestion pipeline) all depend on this new schema. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist.
2. **Breaking API changes** — The service layer and endpoints switch from joining `advisory_status` to querying `advisory.status` directly. These code changes are incompatible with the old schema, and the old code is incompatible with the new schema.
3. **Tightly coupled feature components** — The entity definitions, service layer, endpoints, and ingestion pipeline are all tightly coupled to the schema change. No subset of these changes is independently deployable.

The non-functional requirements explicitly state: "All changes must land together: merging the migration without the code changes would break all advisory queries."

The `workflow:feature-branch` label will be applied to the feature issue TC-9005.

---

## trustify-backend

### changes:
- Create database migration to define `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from existing `status_id` join, drop `status_id` FK column, and drop `advisory_status` lookup table
- Update SeaORM entity definition in `entity/src/advisory.rs` to replace `status_id` foreign key with `status` enum column, and remove `entity/src/advisory_status.rs` entity file
- Update `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` to query `advisory.status` directly instead of joining `advisory_status` table
- Update advisory model structs (`AdvisorySummary`, `AdvisoryDetails`) to source status from the enum column instead of the join
- Update advisory REST endpoints (`list.rs`, `get.rs`) to filter by enum `status` column instead of joined status
- Update advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into lookup table
- Update advisory integration tests in `tests/api/advisory.rs` to reflect new schema and query patterns
- Update `entity/src/lib.rs` to remove `advisory_status` module registration
- Update `migration/src/lib.rs` to register the new migration module

---

## Excluded requirements

None. All requirements from the Feature description can be planned against the trustify-backend repository.
