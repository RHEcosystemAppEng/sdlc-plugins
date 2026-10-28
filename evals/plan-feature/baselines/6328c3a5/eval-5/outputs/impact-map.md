# Repository Impact Map -- TC-9005

## trustify-backend

changes:
  - Create database migration to define `advisory_status_enum` PostgreSQL enum type, add `status` enum column to `advisory` table, backfill from `advisory_status` join, drop `status_id` foreign key column, and drop `advisory_status` lookup table
  - Update SeaORM entity definitions: modify `entity/src/advisory.rs` to replace `status_id` FK with `status` enum field; remove `entity/src/advisory_status.rs` entity
  - Update `AdvisorySummary` and `AdvisoryDetails` model structs to source status from the enum column instead of the join
  - Update `AdvisoryService` query logic to filter and select on the `status` enum column directly, removing the `advisory_status` table join
  - Update advisory list and get endpoints to use enum-based status filtering
  - Update advisory ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`) to write enum values directly instead of inserting into the lookup table
  - Update advisory integration tests (`tests/api/advisory.rs`) to validate enum-based queries, status filtering, and ingestion

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale -- atomicity indicators identified:**

1. **Coordinated schema migrations:** The database migration creates the `advisory_status_enum` type and adds the `status` column that all service-layer code depends on. The migration also drops the `status_id` FK column and `advisory_status` table that the current code uses. These schema changes and code changes are mutually dependent.
2. **Tightly coupled feature components:** Merging the migration without the code changes would break all advisory queries (they still join the now-dropped `advisory_status` table). Merging the code changes without the migration would reference a `status` column that does not exist. The feature's non-functional requirements explicitly state: "All changes must land together."
3. **Cross-cutting refactors:** The entity definition change (`advisory.rs`) propagates through the service layer (`AdvisoryService`), endpoint handlers (list, get), ingestion pipeline, and integration tests. Partial delivery would leave the codebase in an inconsistent state.

**Interdependent tasks:**
- Task 2 (migration) <-> Task 3 (entities): entity definitions must match the new schema
- Task 3 (entities) <-> Task 4 (service/endpoints): service layer uses entity types
- Task 3 (entities) <-> Task 5 (ingestion): ingestion uses entity types
- Task 4/5 (service/ingestion) <-> Task 6 (tests): tests validate the complete flow

The `workflow:feature-branch` label will be applied to the TC-9005 feature issue.

## Additional Fields (propagated to all created issues)

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

- **Priority**: "High" -- inherited from parent Feature TC-9005
- **fixVersions**: "RHTPA 2.0.0" -- inherited from parent Feature TC-9005; `fixVersion scope` is "both" per Jira Field Defaults, so propagated to tasks

## Excluded Requirements

None. All MVP requirements from the Feature description map to actionable tasks within the trustify-backend repository.

## Documentation Signals

- **Doc impact type**: Updates to existing content
- **Details**: Update internal architecture docs to reflect schema change (advisory_status lookup table replaced by enum column)
- **No external API documentation changes needed** -- response shape remains identical
