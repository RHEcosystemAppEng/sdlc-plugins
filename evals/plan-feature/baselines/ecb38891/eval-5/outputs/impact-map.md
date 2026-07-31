# Repository Impact Map -- TC-9005: Drop status table and migrate to enum column

## trustify-backend

### changes:
- Create atomic database migration: define `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from `advisory_status` join, drop `status_id` foreign key column, drop `advisory_status` lookup table
- Update SeaORM entity definition in `entity/src/advisory.rs` to replace `status_id` integer FK with `status` enum column mapped to `advisory_status_enum`; remove `entity/src/advisory_status.rs` entity; update `entity/src/lib.rs` to remove the `advisory_status` module registration
- Update `AdvisorySummary` and `AdvisoryDetails` model structs in `modules/fundamental/src/advisory/model/` to use the enum status field instead of joining the lookup table
- Update `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` to query the `status` enum column directly, removing all `advisory_status` table joins
- Update advisory list and get endpoint handlers in `modules/fundamental/src/advisory/endpoints/` to filter/return status using the enum column
- Update advisory ingestion in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into the lookup table first
- Update query helpers in `common/src/db/query.rs` if advisory status filtering logic exists there
- Update integration tests in `tests/api/advisory.rs` to verify queries against the new enum column

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators are present:

1. **Coordinated schema migrations** -- The database migration adds the `advisory_status_enum` type and `status` column while dropping the `status_id` FK and `advisory_status` table. All code changes (entity, service, endpoints, ingestion) depend on this schema change being present. Merging the migration without the code changes would break all advisory queries (they still reference the now-dropped join). Merging the code changes without the migration would reference a column that does not exist.

2. **Cross-cutting refactors** -- Removing the `advisory_status` join touches the entity layer, service layer, model structs, endpoint handlers, ingestion pipeline, and integration tests. Partial delivery would leave the codebase in an inconsistent state where some code references the old FK and some references the new enum column.

3. **Tightly coupled feature components** -- The feature's non-functional requirements explicitly state: "All changes must land together: merging the migration without the code changes would break all advisory queries, and merging the code changes without the migration would reference a column that does not exist."

**Interdependent tasks:** Tasks 2-6 (migration, entity update, service/endpoint update, ingestion update, integration tests) are all mutually dependent. No single task can be merged to `main` independently without breaking the build.

The `workflow:feature-branch` label will be applied to the feature issue TC-9005.

## Excluded Requirements

None -- all requirements from the Feature description can be decomposed into actionable tasks against the trustify-backend repository.

## Additional Fields (propagated to all created tasks)

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

- **Priority**: "High" -- inherited from Feature TC-9005 (not "Undefined", so propagated)
- **Fix Versions**: "RHTPA 2.0.0" -- inherited from Feature TC-9005 (no `fixVersion scope` setting in Jira Field Defaults, defaulting to "both", so propagated to tasks)
