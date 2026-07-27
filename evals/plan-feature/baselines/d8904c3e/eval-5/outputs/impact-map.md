# Repository Impact Map — TC-9005

## Feature: Drop status table and migrate to enum column

### trustify-backend

changes:
  - Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected) and database migration to add `status` column, backfill from join, drop `status_id` FK and `advisory_status` table
  - Update SeaORM entity definitions: modify `entity/advisory.rs` to use enum column, remove `entity/advisory_status.rs`
  - Update `AdvisoryService` and advisory model structs to query enum column directly instead of joining `advisory_status` table
  - Update advisory endpoints (`list.rs`, `get.rs`) to use new status column without join
  - Update advisory ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`) to write enum values directly instead of lookup table inserts
  - Update advisory integration tests (`tests/api/advisory.rs`) to reflect new schema and query patterns

### Excluded requirements

None — all requirements can be planned with the available repository structure and feature specification.

---

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators were identified:

1. **Coordinated schema migrations** — The database migration creates the enum type, adds the column, backfills data, and drops the old FK column and lookup table. The code changes (entity definitions, service queries, endpoints, ingestion) all depend on this new schema. A partial merge would leave the codebase broken.

2. **Tightly coupled feature components** — The feature's non-functional requirements explicitly state: "All changes must land together: merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist."

**Interdependent tasks:**
- Task 2 (migration) + Task 3 (entity) + Task 4 (service) + Task 5 (endpoints) + Task 6 (ingestion) are all mutually dependent — none can be merged to `main` independently without breaking the application.

The `workflow:feature-branch` label will be applied to the feature issue TC-9005.

---

## Epic Grouping (by-sub-feature)

| Epic | Tasks | Description |
|---|---|---|
| TC-9005: Schema Migration | Tasks 2, 3 | Database migration and SeaORM entity definition updates |
| TC-9005: Advisory Query Layer | Tasks 4, 5 | Service, model, and endpoint updates to use enum column |
| TC-9005: Ingestion & Testing | Tasks 6, 7 | Ingestion pipeline update and integration test coverage |

---

## Field Inheritance

- **Priority:** High (inherited from TC-9005, propagated to all tasks and epics)
- **fixVersions:** RHTPA 2.0.0 (inherited from TC-9005, propagated to all tasks and epics — fixVersion scope defaults to "both" since no Jira Field Defaults section exists in CLAUDE.md)
- **Labels:** `ai-generated-jira` applied to all created issues
- **Feature label:** `workflow:feature-branch` applied to TC-9005

## additional_fields (per created issue)

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```
