# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators were identified:

1. **Coordinated schema migrations** — The migration creates the `advisory_status_enum` type, adds the `status` column, backfills data, drops the `status_id` column, and drops the `advisory_status` table. All code changes depend on this migration completing first, and merging code without the migration would reference a column that does not exist.

2. **Breaking API changes** — The entity definitions change from `status_id: i32` (foreign key) to `status: AdvisoryStatusEnum`. Merging the entity change without the migration would fail at runtime (column does not exist). Merging the migration without the entity change would also fail (code still queries the dropped `status_id` column and `advisory_status` table).

3. **Tightly coupled feature components** — The service layer, ingestion pipeline, and integration tests all depend on the entity definitions, which depend on the migration. Merging any subset would leave the codebase in an inconsistent state.

The feature's Non-Functional Requirements explicitly state: "All changes must land together: merging the migration without the code changes would break all advisory queries, and merging the code changes without the migration would reference a column that does not exist."

**Interdependent tasks:** Tasks 2 (migration), 3 (entity), 4 (service/endpoints), 5 (ingestion), and 6 (tests) are all interdependent. Each depends on the prior layer and none can be merged to `main` independently.

**Label:** The `workflow:feature-branch` label will be applied to the feature issue TC-9005.

---

## Impact Map

trustify-backend:
  changes:
    - Create reversible database migration: define `advisory_status_enum` PostgreSQL type, add `status` enum column to `advisory` table, backfill from `status_id` join, drop `status_id` FK column, drop `advisory_status` lookup table
    - Update SeaORM entity definitions: replace `status_id` integer FK with `status: AdvisoryStatusEnum` on the advisory entity, remove advisory_status entity module
    - Update advisory service layer (AdvisoryService) to query `advisory.status` enum column directly, removing all joins to `advisory_status`
    - Update advisory endpoints (list, get) to filter by enum column instead of joined table
    - Update advisory ingestion pipeline to map incoming status strings to `AdvisoryStatusEnum` and write directly to the `status` column
    - Update advisory integration tests to use enum-based fixtures and assertions
    - Update internal architecture documentation to reflect the schema change

## Excluded Requirements

None. All requirements from the feature description can be addressed within the trustify-backend repository.

---

## Epic Grouping (by-sub-feature)

Per Hierarchy Configuration default (`by-sub-feature`), tasks are grouped into the following logical sub-features:

### Epic 1: TC-9005: Schema migration and entity update
- Task 2 — Create migration for advisory status enum conversion
- Task 3 — Update SeaORM entity definitions for advisory status enum

### Epic 2: TC-9005: Application code updates
- Task 4 — Update advisory service layer and endpoints to use status enum
- Task 5 — Update advisory ingestion pipeline for status enum

### Epic 3: TC-9005: Testing and documentation
- Task 6 — Update advisory integration tests for status enum
- Task 7 — Update internal architecture documentation

---

## Task Creation Details

### additional_fields for all tasks

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

- **Priority**: inherited from Feature TC-9005 (High)
- **fixVersions**: inherited from Feature TC-9005 (RHTPA 2.0.0); `fixVersion scope` not configured in Jira Field Defaults, defaulting to `"both"` (propagate to tasks)

### Feature issue label update

After all tasks are created, the `workflow:feature-branch` label will be appended to TC-9005's existing labels:
- Existing labels: `["ai-generated-jira"]`
- Updated labels: `["ai-generated-jira", "workflow:feature-branch"]`
