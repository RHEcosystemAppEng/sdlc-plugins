# Repository Impact Map — TC-9005

## trustify-backend

### changes:
- Create database migration to define `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from `advisory_status` join, drop `status_id` foreign key column, and drop `advisory_status` lookup table — all in a single atomic migration
- Update SeaORM entity `entity/src/advisory.rs` to replace `status_id` foreign key field with a `status` enum field of type `advisory_status_enum`
- Remove SeaORM entity file `entity/src/advisory_status.rs` (the lookup table entity is no longer needed)
- Update `entity/src/lib.rs` to remove the `advisory_status` module re-export
- Update `modules/fundamental/src/advisory/service/advisory.rs` (AdvisoryService) to query `advisory.status` directly instead of joining `advisory_status` table
- Update `modules/fundamental/src/advisory/model/summary.rs` (AdvisorySummary) to source status from the enum column instead of the join
- Update `modules/fundamental/src/advisory/model/details.rs` (AdvisoryDetails) to source status from the enum column instead of the join
- Update `modules/fundamental/src/advisory/endpoints/list.rs` to filter by enum column instead of joining advisory_status
- Update `modules/fundamental/src/advisory/endpoints/get.rs` to read status from enum column
- Update `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly to the `status` column instead of inserting into the lookup table
- Update `common/src/db/query.rs` if advisory status filtering helpers reference the old join pattern
- Update `tests/api/advisory.rs` to reflect the new schema (no join, enum column filtering)

## Workflow Mode

**Mode:** `feature-branch`

**Rationale:** Atomicity indicator "Coordinated schema migrations" is present. The database migration adds the `status` enum column and drops the `advisory_status` table and `status_id` FK column. Without the corresponding code changes, all advisory queries would attempt to join a table that no longer exists. Conversely, merging the code changes without the migration would reference a `status` column that does not yet exist. The non-functional requirements explicitly state: "All changes must land together." Tasks 2-5 (entity updates, service/endpoint updates, ingestion updates, tests) are all interdependent with Task 1 (migration).
