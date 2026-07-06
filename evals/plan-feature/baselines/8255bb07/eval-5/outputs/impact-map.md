# Repository Impact Map

## trustify-backend

### Changes

- Create database migration to add `advisory_status_enum` PostgreSQL type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table backfilled from `advisory_status` join, drop `status_id` foreign key column, and drop `advisory_status` lookup table
- Update SeaORM entity definitions: modify `entity/src/advisory.rs` to replace `status_id` foreign key with `status` enum column, remove `entity/src/advisory_status.rs` entity, update `entity/src/lib.rs` module registration
- Update advisory service queries in `modules/fundamental/src/advisory/service/advisory.rs` to use `status` enum column directly instead of joining `advisory_status` table
- Update advisory model structs in `modules/fundamental/src/advisory/model/summary.rs` and `modules/fundamental/src/advisory/model/details.rs` to reflect the new status field type
- Update advisory endpoint handlers in `modules/fundamental/src/advisory/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/get.rs` to use updated service and model layer
- Update advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into lookup table
- Update advisory integration tests in `tests/api/advisory.rs` to verify queries and endpoints work with the new enum-based status

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migrations** -- The migration adds the `advisory_status_enum` type and `status` column while dropping the `status_id` FK and `advisory_status` table. The code changes in the entity definitions, service layer, and ingestion pipeline all depend on this new schema being in place.
2. **Breaking API changes** -- Dropping the `advisory_status` table and `status_id` FK column would break all advisory queries that join on the lookup table if the code changes are not deployed simultaneously.
3. **Tightly coupled feature components** -- The migration, entity definitions, service layer, endpoint handlers, and ingestion pipeline form a dependency chain where no single piece functions correctly without the others. Merging the migration alone would break all advisory queries; merging the code changes alone would reference a column that does not exist.

**Interdependent tasks:**
- Task 2 (migration) creates the schema that Tasks 3-6 depend on
- Task 3 (entities) provides the data model that Tasks 4 and 5 require
- Tasks 4 and 5 (service/endpoints and ingestion) cannot function without the entity and migration changes
- Task 6 (tests) validates the combined behavior of all preceding changes

The `workflow:feature-branch` label will be applied to the feature issue TC-9005.

## Excluded Requirements

None. All requirements from the Feature description are addressable within the trustify-backend repository.
