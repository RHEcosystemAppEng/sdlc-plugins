# Repository Impact Map -- TC-9005

## Feature
**TC-9005**: Drop status table and migrate to enum column

## Workflow Mode

**feature-branch**

**Rationale:** This feature requires feature-branch mode based on the following atomicity indicators:

1. **Coordinated schema migration** -- The database migration creates the `advisory_status_enum` type, adds and backfills the `status` column, and drops the `advisory_status` lookup table. The code changes (entity definitions, service queries, ingestion pipeline) depend on the new schema being present. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped table). Merging the code changes without the migration would reference a column that does not exist.
2. **Cross-cutting refactor** -- Removing the `advisory_status` entity and all references to `status_id` spans multiple modules (entity, fundamental/advisory service, fundamental/advisory endpoints, ingestor, search, tests). Partial delivery would leave the codebase with broken imports and unresolved references.

**Interdependent tasks:** Tasks 2 (migration), 3 (entity), 4 (service/endpoints), and 5 (ingestion) form a tightly coupled chain -- the migration creates the schema that the entity layer maps, the entity layer defines the types that the service and ingestion layers consume.

The `workflow:feature-branch` label will be applied to the feature issue TC-9005.

## Inherited Field Values

| Field | Value | Propagation |
|---|---|---|
| Priority | High | Propagated to all created issues (Feature priority is set and not "Undefined") |
| Fix Versions | RHTPA 2.0.0 | Propagated to all created issues (fixVersion scope: "both" -- default, no Jira Field Defaults section configured) |
| Labels | ai-generated-jira | Applied to all created issues |

### additional_fields for created issues

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

## Repository: trustify-backend

### Changes

- Create reversible database migration: create `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from existing `advisory_status` join, drop `status_id` FK column, drop `advisory_status` lookup table
- Update SeaORM entity definitions: define `AdvisoryStatusEnum` enum in `entity/src/advisory.rs` using `DeriveActiveEnum`, remove `entity/src/advisory_status.rs`, update `entity/src/lib.rs` exports
- Update advisory service layer: remove all `advisory_status` table joins from advisory queries in `AdvisoryService`, use direct enum column for status filtering
- Update advisory endpoint handlers: modify list and get handlers to read status from enum column instead of join result
- Update search service: check and update any `advisory_status` references in `SearchService` full-text search
- Update advisory ingestion pipeline: write `AdvisoryStatusEnum` values directly to `advisory.status` column instead of inserting into lookup table
- Update advisory integration tests: use enum values in test data setup, verify status filtering, verify backward-compatible response shape
- Update internal architecture documentation: reflect schema change from lookup table to enum column

## Epic Grouping (by-sub-feature)

| Epic | Summary | Tasks |
|---|---|---|
| TC-9005: Database schema migration | Migration and entity layer changes for the advisory status enum conversion | Task 2, Task 3 |
| TC-9005: Application layer updates | Service, endpoint, and ingestion pipeline changes to use the new enum column | Task 4, Task 5 |
| TC-9005: Verification and documentation | Integration test updates and architecture documentation | Task 6, Task 7 |

Bookend tasks (Task 1: create-branch, Task 8: merge-branch) are not assigned to Epics.

## Task Summary

| # | Summary | Type | Target Branch | Epic | Dependencies |
|---|---|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | Bookend (create-branch) | main | -- | None |
| 2 | Create database migration for advisory status enum conversion | Implementation | TC-9005 | Database schema migration | Task 1 |
| 3 | Update SeaORM entity definitions for advisory status enum | Implementation | TC-9005 | Database schema migration | Task 1, Task 2 |
| 4 | Update advisory service and endpoints to use status enum | Implementation | TC-9005 | Application layer updates | Task 1, Task 3 |
| 5 | Update advisory ingestion pipeline for direct enum writes | Implementation | TC-9005 | Application layer updates | Task 1, Task 3 |
| 6 | Update advisory integration tests for status enum | Implementation | TC-9005 | Verification and documentation | Task 1, Task 4, Task 5 |
| 7 | Update internal architecture documentation | Documentation | TC-9005 | Verification and documentation | Task 4, Task 5, Task 6 |
| 8 | Merge feature branch TC-9005 to main | Bookend (merge-branch) | main | -- | Task 2, Task 3, Task 4, Task 5, Task 6 |

## Excluded Requirements

None -- all requirements from the feature description can be planned with the available repository structure.
