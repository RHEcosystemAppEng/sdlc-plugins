# Repository Impact Map -- TC-9005

## trustify-backend

### changes:
- Create database migration to define `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from existing `status_id` join, drop `status_id` foreign key column, and drop `advisory_status` lookup table -- all in a single atomic, reversible migration
- Update SeaORM entity definition in `entity/src/advisory.rs` to replace the `status_id` foreign key field with a `status` enum field of type `advisory_status_enum`
- Remove SeaORM entity definition `entity/src/advisory_status.rs` (the lookup table entity) and remove its registration from `entity/src/lib.rs`
- Update `AdvisorySummary` and `AdvisoryDetails` model structs in `modules/fundamental/src/advisory/model/` to use the enum `status` field instead of joining `advisory_status`
- Update `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` to query the `status` enum column directly, removing all `advisory_status` table joins
- Update advisory list and get endpoints in `modules/fundamental/src/advisory/endpoints/` to use the new `status` column for filtering (WHERE status = 'Fixed' instead of JOIN + WHERE)
- Update advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into the lookup table first
- Update advisory integration tests in `tests/api/advisory.rs` to reflect the new schema (enum column, no join, no lookup table)

## Excluded requirements

None -- all requirements from the Feature description can be decomposed into actionable tasks against the trustify-backend repository.

---

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators are present:

1. **Coordinated schema migration** -- The database migration adds the `advisory_status_enum` type and `status` column, backfills data, drops the `status_id` FK column, and drops the `advisory_status` table. All code changes (entity definitions, service layer, endpoints, ingestion pipeline) depend on this migration having run. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped `advisory_status` table). Merging the code changes without the migration would reference a `status` column that does not exist.

2. **Breaking API changes (internal)** -- The entity layer change (removing `advisory_status.rs`, changing `advisory.rs` to use an enum field) is consumed by the service layer and endpoints. Partial delivery would leave the service layer referencing a removed entity or a nonexistent field.

3. **Cross-cutting refactor** -- The removal of the `advisory_status` join touches the entity layer, service layer, endpoints, ingestion pipeline, and tests simultaneously. No subset of these changes produces a working codebase.

**Interdependent tasks:** All implementation tasks (migration, entity update, entity removal, model update, service update, endpoint update, ingestion update, test update) are mutually dependent -- none can be merged to `main` independently without breaking the build.

The `workflow:feature-branch` label will be applied to the feature issue TC-9005.
