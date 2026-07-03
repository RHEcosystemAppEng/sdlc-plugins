# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## trustify-backend

### Changes
- Create reversible database migration: define `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from existing `status_id` join, drop `status_id` FK column, drop `advisory_status` lookup table
- Update SeaORM entity `entity/src/advisory.rs`: replace `status_id` integer FK field with `status` enum column using SeaORM enum mapping
- Remove SeaORM entity for the `advisory_status` lookup table and its registration in `entity/src/lib.rs`
- Update `AdvisorySummary` and `AdvisoryDetails` model structs in `modules/fundamental/src/advisory/model/` to use enum status directly instead of resolving via lookup table join
- Update `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` to remove `advisory_status` table join from all queries, filter directly on enum column
- Update advisory list endpoint in `modules/fundamental/src/advisory/endpoints/list.rs` and get endpoint in `get.rs` to filter and return status using the enum column
- Update advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into `advisory_status` lookup table
- Update advisory integration tests in `tests/api/advisory.rs` for the new schema

## Excluded Requirements

None — all seven MVP requirements from the Feature description are plannable within the trustify-backend repository.

## Workflow Mode

**Mode**: `feature-branch`

**Rationale**: Multiple atomicity indicators are present:
1. **Coordinated schema migrations** — The database migration creates the enum column and drops the `status_id` FK column and `advisory_status` table. All code changes (entity, service, endpoints, ingestion) depend on this new schema. Merging the migration without code changes would break queries that still join the dropped table. Merging code changes without the migration would reference a non-existent `status` column.
2. **Cross-cutting refactors** — Entity definitions, model structs, service layer, endpoints, and ingestion pipeline all reference the status field structure. Partial delivery would leave the codebase in an inconsistent state.

The Feature's non-functional requirements explicitly state: "All changes must land together."

**Interdependent tasks**: All implementation tasks (migration, entity, models, service, endpoints, ingestion, tests) are interdependent — each depends on the schema change and none functions correctly in isolation on `main`.

The `workflow:feature-branch` label will be applied to the TC-9005 feature issue.

## Epic Grouping (by-sub-feature)

| Epic | Summary | Tasks |
|---|---|---|
| A | TC-9005: Database Schema & Entity Layer | Task 2 (migration), Task 3 (entities) |
| B | TC-9005: Advisory Query & API Updates | Task 4 (models), Task 5 (service), Task 6 (endpoints) |
| C | TC-9005: Ingestion Pipeline & Validation | Task 7 (ingestion), Task 8 (tests), Task 9 (documentation) |

Bookend tasks (Task 1: create-branch, Task 10: merge-branch) are not assigned to Epics.

## Issue Type Mapping

| Role | Type Name | Hierarchy Level |
|---|---|---|
| Feature | Feature | 2 |
| Epic | Epic | 1 |
| Task | Task | 0 |

## Task Creation Log — additional_fields

### Epics

All Epics are created with `parent: TC-9005` (the Feature issue) and the following `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

### Tasks

All Tasks are created with `parent: <assigned-epic-key>` and the following `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

Bookend tasks (Task 1, Task 10) are created with no Epic parent but with the same `additional_fields`.

**Rationale**:
- `priority`: inherited from Feature TC-9005 (priority: "High", not "Undefined")
- `fixVersions`: inherited from Feature TC-9005 (RHTPA 2.0.0); no `fixVersion scope` setting in Jira Field Defaults section, defaulting to "both" (propagate to tasks)
- `labels`: `ai-generated-jira` is always included per skill rules

### Feature Issue Updates
- Add `workflow:feature-branch` label to TC-9005's existing labels: `["ai-generated-jira", "workflow:feature-branch"]`

## Issue Link Plan

### Feature "incorporates" Epics
- TC-9005 **incorporates** Epic A (TC-9005: Database Schema & Entity Layer)
- TC-9005 **incorporates** Epic B (TC-9005: Advisory Query & API Updates)
- TC-9005 **incorporates** Epic C (TC-9005: Ingestion Pipeline & Validation)

### Task dependency links ("depends on")
- Task 2 depends on Task 1 (create-branch)
- Task 3 depends on Task 1, Task 2
- Task 4 depends on Task 1, Task 3
- Task 5 depends on Task 1, Task 4
- Task 6 depends on Task 1, Task 5
- Task 7 depends on Task 1, Task 3
- Task 8 depends on Task 1, Task 5, Task 6, Task 7
- Task 9 depends on Tasks 2, 3, 5, 6, 7, 8
- Task 10 depends on Tasks 2, 3, 4, 5, 6, 7, 8, 9
