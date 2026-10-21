# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migrations** — The database migration creates a new enum type, adds an enum column, backfills data, drops the FK column, and drops the lookup table. All code changes (entity definitions, service queries, ingestion pipeline) depend on this migration having run. Merging the migration alone would drop the table that existing queries still join.

2. **Breaking API changes** — The migration removes the `advisory_status` table and the `status_id` FK column. Any code that still references `advisory.status_id` or joins `advisory_status` would break if merged without the corresponding code updates. Conversely, code referencing `advisory.status` (the new enum column) would break if merged before the migration.

3. **Tightly coupled feature components** — The entity layer, service layer, endpoints, and ingestion pipeline all depend on the same schema change. No individual change is safe to merge to `main` independently.

**Interdependent tasks:**
- Migration task creates the enum type and column that all other tasks depend on
- Entity definition update removes `advisory_status.rs` and changes `advisory.rs` — service and endpoint tasks consume these entities
- Service/endpoint query updates and ingestion pipeline updates both depend on the entity changes
- All changes must land together per the feature's non-functional requirements

**Label decision:** The `workflow:feature-branch` label will be applied to the TC-9005 feature issue.

---

## Impact Map

trustify-backend:
  changes:
    - Create database migration to define `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from `status_id` join, drop `status_id` FK column, and drop `advisory_status` lookup table
    - Update SeaORM entity definition in `entity/src/advisory.rs` to replace `status_id: i32` FK column with `status: AdvisoryStatusEnum` enum column, and remove `entity/src/advisory_status.rs` entity file
    - Update `entity/src/lib.rs` to remove `advisory_status` module re-export
    - Update `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` to query `advisory.status` directly instead of joining `advisory_status`
    - Update `AdvisorySummary` and `AdvisoryDetails` models in `modules/fundamental/src/advisory/model/` to use the enum column instead of joined status
    - Update advisory list and get endpoints in `modules/fundamental/src/advisory/endpoints/` to filter by enum column instead of joining the lookup table
    - Update advisory ingestion in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into the lookup table
    - Update advisory integration tests in `tests/api/advisory.rs` to reflect the new schema (enum column, no join, no lookup table)
    - Update `common/src/db/query.rs` if advisory status filtering logic is shared there

## Documentation Impact

- **Doc impact type:** Updates to existing content
- **Details:** Minor — update internal architecture docs to reflect schema change. No external API documentation changes needed.

## Excluded Requirements

None — all requirements from the feature description can be planned with the available repository structure and specification.

## Epic Grouping (by-sub-feature)

- **TC-9005: Database Schema Migration** — migration task
- **TC-9005: Entity and Query Layer** — entity definitions, service layer, and endpoint updates
- **TC-9005: Ingestion and Testing** — ingestion pipeline update, integration tests, and documentation
