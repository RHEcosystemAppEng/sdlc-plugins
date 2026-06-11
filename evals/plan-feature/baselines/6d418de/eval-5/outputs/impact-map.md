# Repository Impact Map — TC-9005

## Feature: Drop status table and migrate to enum column

### Workflow Mode: `feature-branch`

**Rationale:** This feature triggers multiple atomicity indicators:

1. **Coordinated schema migration** — The database migration adds the `advisory_status_enum` type and `status` enum column, backfills data, then drops the `status_id` FK column and the `advisory_status` lookup table. The code changes (entity definitions, service layer, endpoints, ingestion pipeline) depend on the new schema. Merging the migration alone would drop the table that existing queries still join; merging the code alone would reference a column that does not exist.

2. **Breaking API changes (internal)** — The SeaORM entity for `advisory` changes from a `status_id: i32` foreign key to a `status: AdvisoryStatusEnum` enum field. Every consumer of the `Advisory` entity (service layer, endpoints, ingestion) must be updated atomically.

3. **Tightly coupled feature components** — The migration, entity layer, service layer, endpoint layer, and ingestion pipeline are all interdependent. No single component functions correctly without the others being updated simultaneously.

**Interdependent tasks:** All intermediate tasks (migration, entity update, service/endpoint update, ingestion update, tests) are mutually dependent and must land on the feature branch before merging to `main`.

---

### trustify-backend

**Changes:**

- Create a reversible database migration that: defines `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected); adds `status` enum column to `advisory` table; backfills `status` from the `advisory_status` join; drops `status_id` FK column; drops `advisory_status` lookup table
- Update SeaORM entity `entity/src/advisory.rs` to replace `status_id: i32` FK field with `status: AdvisoryStatusEnum` enum field
- Remove SeaORM entity file `entity/src/advisory_status.rs` (the lookup table entity)
- Update `entity/src/lib.rs` to remove the `advisory_status` module export
- Update `modules/fundamental/src/advisory/service/advisory.rs` (AdvisoryService) to query by `advisory.status` enum column instead of joining `advisory_status`
- Update `modules/fundamental/src/advisory/model/summary.rs` (AdvisorySummary) to source status from the enum column
- Update `modules/fundamental/src/advisory/model/details.rs` (AdvisoryDetails) to source status from the enum column
- Update `modules/fundamental/src/advisory/endpoints/list.rs` to filter by enum column instead of join
- Update `modules/fundamental/src/advisory/endpoints/get.rs` to read status from enum column
- Update `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into lookup table
- Update `common/src/db/query.rs` if advisory status filtering helpers reference the join
- Update integration tests in `tests/api/advisory.rs` to reflect the new schema
- Update `README.md` or architecture docs if they reference the `advisory_status` table
