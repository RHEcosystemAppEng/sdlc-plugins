# Repository Impact Map — TC-9005

## trustify-backend

### Changes

- Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected) via a new reversible migration
- Backfill the new `status` enum column on the `advisory` table from the existing `status_id` join
- Drop the `status_id` foreign key column from the `advisory` table
- Drop the `advisory_status` lookup table
- Update the SeaORM `Advisory` entity to replace `status_id` (integer FK) with `status` (DeriveActiveEnum mapped to `advisory_status_enum`)
- Remove the SeaORM entity file for the `advisory_status` lookup table and its re-export from `entity/src/lib.rs`
- Update `AdvisorySummary` and `AdvisoryDetails` model structs to use the new enum type instead of a joined status value
- Remove `advisory_status` table JOINs from `AdvisoryService` fetch, list, and search methods; query the `status` column directly
- Update advisory list endpoint status filter to accept enum string values instead of integer status IDs
- Update advisory ingestion pipeline to write enum values directly instead of inserting into the lookup table first
- Update integration tests for advisory endpoints and search to use the new enum column and remove lookup table fixtures
- Register the new migration module in `migration/src/lib.rs`

## Workflow Mode

**Selected mode: `feature-branch`**

**Rationale:** Three atomicity indicators are present:

1. **Coordinated schema migration** — The database migration adds the `status` enum column and drops the `advisory_status` table. All code changes (entity definitions, service queries, ingestion pipeline) depend on this migration having run. Merging the migration without the code changes would break all advisory queries (they would still attempt to JOIN the now-dropped table). Merging the code changes without the migration would reference a column (`status`) that does not yet exist.

2. **Breaking API changes** — The entity layer changes from `status_id: i32` (FK) to `status: AdvisoryStatusEnum`. All consumers of the entity (services, endpoints, ingestor) must update simultaneously. A partial merge would produce compile errors.

3. **Cross-cutting refactor** — The removal of the `advisory_status` JOIN spans the entity layer, service layer, endpoint layer, and ingestion module. Partial delivery leaves the codebase in an inconsistent state where some code paths reference the dropped table and others reference the new column.

The feature's non-functional requirements explicitly state: "All changes must land together."

**Interdependent tasks:** All intermediate implementation tasks (migration, entity update, service update, endpoint update, ingestion update, test update) are mutually dependent and must merge into the feature branch before the final merge to main.
