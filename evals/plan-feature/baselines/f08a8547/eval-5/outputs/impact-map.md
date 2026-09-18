# Repository Impact Map -- TC-9005: Drop status table and migrate to enum column

## trustify-backend

### Changes
- Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected) via a reversible database migration
- Add `status` enum column to `advisory` table, backfilled from the existing `status_id` foreign key join
- Drop `status_id` foreign key column from `advisory` table
- Drop `advisory_status` lookup table after all references are removed
- Update SeaORM entity `entity/src/advisory.rs` to define `AdvisoryStatusEnum` and replace `status_id` column with `status` enum column
- Remove SeaORM entity for `advisory_status` (remove module reference in `entity/src/lib.rs`)
- Update `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` to query `status` column directly instead of joining `advisory_status` table
- Update advisory model structs (`AdvisorySummary` in `summary.rs`, `AdvisoryDetails` in `details.rs`) to source status from enum column
- Update advisory endpoint handlers (`list.rs`, `get.rs`) for enum-based status filtering
- Update advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into lookup table
- Update advisory integration tests in `tests/api/advisory.rs` for enum-based schema
- Update internal architecture documentation to reflect schema change

### Excluded Requirements
None -- all requirements from the feature description can be planned with the available repository structure and information.

## Workflow Mode Decision

**Selected mode: feature-branch**

Atomicity indicators found:

1. **Coordinated schema migration** -- the migration adds the `status` enum column and drops the `advisory_status` lookup table and `status_id` FK column. If the migration lands without the code changes, all advisory queries that join the now-dropped table will fail. If the code changes land without the migration, they reference a `status` column that does not exist.

2. **Breaking API changes** -- the service layer, endpoint handlers, and ingestion pipeline reference the new `status` enum column. The old code references `status_id` and the `advisory_status` table. Partial delivery in either direction breaks the application at the data layer.

3. **Explicit atomicity requirement** -- the feature description's Non-Functional Requirements state: "All changes must land together: merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist."

Interdependent tasks: Tasks 2 (migration), 3 (entities), 4 (service/endpoints), 5 (ingestion), and 6 (tests) are all tightly coupled -- each depends on the schema change and cannot be merged independently to `main` without breaking the application.

The `workflow:feature-branch` label will be applied to feature issue TC-9005.

## Field Inheritance

- **Priority**: Critical -- inherited from parent Feature TC-9005, propagated to all created tasks via `additional_fields`
- **fixVersions**: RHTPA 2.0.0 -- inherited from parent Feature TC-9005, propagated to all created tasks via `additional_fields` (fixVersion scope defaults to "both" -- no `Jira Field Defaults` override present in CLAUDE.md)

### additional_fields applied to each created task

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```
