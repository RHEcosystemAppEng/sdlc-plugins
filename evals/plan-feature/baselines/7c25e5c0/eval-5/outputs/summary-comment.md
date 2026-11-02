# Plan Summary — TC-9005: Drop status table and migrate to enum column

## Tasks Created

| # | Summary | Repository | Target Branch | Jira Key |
|---|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | trustify-backend | main | (pending) |
| 2 | Database migration — create advisory_status_enum and migrate data | trustify-backend | TC-9005 | (pending) |
| 3 | Update SeaORM entity definitions | trustify-backend | TC-9005 | (pending) |
| 4 | Update advisory service and endpoints | trustify-backend | TC-9005 | (pending) |
| 5 | Update advisory ingestion pipeline | trustify-backend | TC-9005 | (pending) |
| 6 | Update integration tests | trustify-backend | TC-9005 | (pending) |
| 7 | Update internal architecture documentation | trustify-backend | TC-9005 | (pending) |
| 8 | Merge feature branch TC-9005 to main | trustify-backend | main | (pending) |

## Repositories Affected

- **trustify-backend** — all changes are within this single repository

## Architecture Summary

This plan replaces the `advisory_status` lookup table with a PostgreSQL enum column (`advisory_status_enum`) directly on the `advisory` table. The migration backfills existing data, drops the FK column and lookup table, and all downstream code (entities, service layer, endpoints, ingestion, tests) is updated to use the enum column. A feature-branch workflow is used because the migration and code changes are interdependent — merging either without the other would break advisory functionality.

## Workflow Mode

**Feature-branch** — all tasks target branch `TC-9005` (except bookend tasks which target `main`). The `workflow:feature-branch` label will be applied to the Feature issue.

## Inherited Field Propagation

| Field | Feature Value | Propagated | Reason |
|---|---|---|---|
| **Priority** | High | Yes | Feature priority is set (not "Undefined") — inherited by all created tasks via `additional_fields.priority` |
| **fixVersions** | RHTPA 2.0.0 | Yes | Feature has non-empty fixVersions array, and fixVersion scope defaults to "both" (no explicit `fixVersion scope` setting in Jira Field Defaults section) — inherited by all created tasks via `additional_fields.fixVersions` |

All created tasks include:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```
