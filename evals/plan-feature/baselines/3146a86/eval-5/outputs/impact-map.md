# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## trustify-backend

### Changes

- Create a new database migration that defines the `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), adds a `status` enum column to the `advisory` table, backfills it from the existing `advisory_status` join, drops the `status_id` foreign key column, and drops the `advisory_status` lookup table — all within a single reversible migration
- Update the SeaORM entity definition in `entity/src/advisory.rs` to replace the `status_id` foreign key field with a `status` enum field mapped to `advisory_status_enum`
- Remove the SeaORM entity file `entity/src/advisory_status.rs` and its registration in `entity/src/lib.rs`
- Update `modules/fundamental/src/advisory/service/advisory.rs` (AdvisoryService) to query the `status` enum column directly instead of joining `advisory_status`
- Update `modules/fundamental/src/advisory/model/summary.rs` (AdvisorySummary) and `modules/fundamental/src/advisory/model/details.rs` (AdvisoryDetails) to source status from the enum column instead of the joined table
- Update `modules/fundamental/src/advisory/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/get.rs` to filter/return status from the enum column
- Update `modules/ingestor/src/graph/advisory/mod.rs` to write the enum value directly on advisory insert instead of inserting into the lookup table
- Update `common/src/db/query.rs` if advisory status filtering logic is shared there
- Update advisory integration tests in `tests/api/advisory.rs` to validate queries against the enum column

---

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migration** — The migration drops the `advisory_status` table and `status_id` column while adding the `status` enum column. Code changes that remove the join and reference the new column cannot be merged independently of the migration. A partial merge would leave the database schema inconsistent with the application code.

2. **Breaking API changes (internal)** — The SeaORM entity changes (removing `advisory_status.rs`, changing `advisory.rs` to use the enum field) would break all advisory service and endpoint code if merged without the corresponding service/endpoint updates.

3. **Cross-cutting refactor** — The status representation change touches the migration, entity layer, service layer, endpoint layer, ingestion pipeline, and tests. Merging any subset to `main` without the rest would produce a broken build or broken queries.

**Interdependent tasks:** All intermediate tasks (migration, entity update, service/endpoint update, ingestion update, tests) are mutually dependent — none can be merged to `main` independently without breaking the application.
