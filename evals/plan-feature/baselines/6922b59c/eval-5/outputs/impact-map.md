# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## trustify-backend

changes:
  - Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected) and a reversible migration that adds a `status` enum column to the `advisory` table, backfills from the existing `status_id` join, drops the `status_id` foreign key column, and drops the `advisory_status` lookup table
  - Update SeaORM entity definitions: modify `entity/src/advisory.rs` to replace the `status_id` foreign key with a `status` enum field, remove `entity/src/advisory_status.rs`, and update `entity/src/lib.rs` to remove the advisory_status module registration
  - Update advisory service layer (`modules/fundamental/src/advisory/service/advisory.rs`) to query the `status` column directly instead of joining the `advisory_status` table
  - Update advisory model structs (`modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/advisory/model/details.rs`) to use the enum type for status
  - Update advisory endpoints (`modules/fundamental/src/advisory/endpoints/list.rs`, `modules/fundamental/src/advisory/endpoints/get.rs`) to filter and return status from the enum column
  - Update advisory ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`) to write enum values directly instead of inserting into the lookup table
  - Update advisory integration tests (`tests/api/advisory.rs`) to verify the new enum-based status behavior

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale — atomicity indicators identified:**

1. **Coordinated schema migrations** — the migration creates the enum type, adds the column, backfills data, drops the FK column, and drops the lookup table. The code changes (entity definitions, service layer, endpoints, ingestion pipeline) depend on the migration having completed. Merging the migration alone would leave dead schema artifacts; merging the code alone would reference a column that does not exist.

2. **Tightly coupled feature components** — the feature description explicitly states: "All changes must land together: merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist."

3. **Breaking API changes** — the entity model change (removing `status_id` FK, adding `status` enum) breaks the service layer and endpoint code that currently joins the lookup table. Partial delivery would leave the application unable to compile or serve requests.

**Interdependent tasks:** All implementation tasks (migration, entity updates, service/endpoint updates, ingestion pipeline updates, test updates) are mutually dependent — no subset can be merged to `main` independently without breaking the build or runtime behavior.

**Label:** The `workflow:feature-branch` label will be applied to the TC-9005 feature issue.

## Excluded Requirements

None — all requirements from the feature description can be decomposed into actionable tasks within the trustify-backend repository.

## Additional Fields for Created Issues

All created tasks will include the following `additional_fields`:

```
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

- **priority**: inherited from Feature TC-9005 (High)
- **fixVersions**: inherited from Feature TC-9005 (RHTPA 2.0.0); `fixVersion scope` not set in Jira Field Defaults, defaulting to "both" (propagate to tasks)

## Epic Grouping (by-sub-feature)

Per CLAUDE.md Hierarchy Configuration (`Default epic grouping strategy: by-sub-feature`):

- **Epic 1: TC-9005: Schema Migration** — Tasks 2 (database migration), 3 (entity definitions)
- **Epic 2: TC-9005: Application Code Updates** — Tasks 4 (service/endpoints), 5 (ingestion pipeline), 6 (integration tests)
- Documentation task (Task 7) assigned to Epic 2
