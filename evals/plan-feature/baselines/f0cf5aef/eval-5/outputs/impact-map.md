# Repository Impact Map — TC-9005

## trustify-backend

changes:
  - Create reversible database migration: define `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from existing `status_id` join, drop `status_id` foreign key column, drop `advisory_status` lookup table
  - Update SeaORM entity definitions: modify `entity/src/advisory.rs` to replace `status_id` foreign key with `status` enum column; remove `entity/src/advisory_status.rs` entity; update `entity/src/lib.rs` exports
  - Update advisory service layer (`modules/fundamental/src/advisory/service/advisory.rs`) to query `status` column directly instead of joining `advisory_status` table
  - Update advisory model structs (`modules/fundamental/src/advisory/model/summary.rs`, `details.rs`) to reflect enum-based status field
  - Update advisory endpoints (`modules/fundamental/src/advisory/endpoints/list.rs`, `get.rs`) to use direct status column for filtering and display
  - Update shared query helpers (`common/src/db/query.rs`) if advisory status filtering logic exists there
  - Update search service (`modules/search/src/service/mod.rs`) if advisory status is indexed for full-text search
  - Update advisory ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`) to write enum values directly instead of inserting into lookup table
  - Update advisory integration tests (`tests/api/advisory.rs`) for new status query patterns

## Excluded requirements

None — all requirements from TC-9005 can be addressed within the trustify-backend repository.

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migration** — The database migration adds the `status` enum column and drops the `status_id` FK column and `advisory_status` table. Code that still joins the dropped table would break if the migration lands first; code referencing the new `status` column would break if the code lands without the migration.
2. **Breaking internal API changes** — The SeaORM entity definition change (replacing `status_id` relation with `status` enum field) is consumed by the advisory service, endpoints, ingestion pipeline, and search service. Merging entity changes without updating all consumers would cause compilation failures.
3. **Explicit NFR** — The feature's non-functional requirements state: "All changes must land together: merging the migration without the code changes would break all advisory queries, and merging the code changes without the migration would reference a column that does not exist."

**Interdependent tasks:** All implementation tasks (migration, entity updates, service/endpoint updates, ingestion updates, tests) are mutually dependent — none can be merged to `main` independently without breaking the application. The `workflow:feature-branch` label will be applied to TC-9005.

## Epic Grouping

**Strategy:** by-sub-feature (from CLAUDE.md Hierarchy Configuration)

| Epic | Sub-feature | Tasks |
|---|---|---|
| TC-9005: Schema and entity migration | Database schema changes and SeaORM entity updates | Task 1 (create branch), Task 2 (migration), Task 3 (entities) |
| TC-9005: Service and ingestion updates | Advisory service, endpoints, and ingestion pipeline | Task 4 (service/endpoints), Task 5 (ingestion) |
| TC-9005: Verification and delivery | Testing, documentation, and merge | Task 6 (tests), Task 7 (documentation), Task 8 (merge branch) |

## Task Creation Fields

All created issues (Epics and Tasks) will include these `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

- **priority**: inherited from TC-9005 (High)
- **fixVersions**: inherited from TC-9005 (RHTPA 2.0.0); `fixVersion scope` defaults to "both" (no Jira Field Defaults section in CLAUDE.md), so fixVersions are propagated to tasks
- **labels**: `ai-generated-jira` applied to all created issues

The feature issue TC-9005 will also receive the `workflow:feature-branch` label (appended to existing labels: `["ai-generated-jira", "workflow:feature-branch"]`).
