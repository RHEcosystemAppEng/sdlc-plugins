# Plan Summary — TC-9005: Drop status table and migrate to enum column

## Tasks Created

| # | Summary | Repository | Target Branch |
|---|---------|-----------|---------------|
| 1 | Create feature branch TC-9005 from main | trustify-backend | main |
| 2 | Database migration: enum column | trustify-backend | TC-9005 |
| 3 | Update entity definitions | trustify-backend | TC-9005 |
| 4 | Update advisory service and endpoints | trustify-backend | TC-9005 |
| 5 | Update ingestion pipeline | trustify-backend | TC-9005 |
| 6 | Update integration tests | trustify-backend | TC-9005 |
| 7 | Merge feature branch TC-9005 to main | trustify-backend | main |

## Repositories Affected

- **trustify-backend** — all tasks target this single repository

## Architecture Summary

This plan replaces the `advisory_status` lookup table with a PostgreSQL enum column (`advisory_status_enum`) directly on the `advisory` table. The change spans the full stack: database migration, SeaORM entity definitions, advisory service/endpoints, ingestion pipeline, and integration tests. The feature-branch workflow ensures all changes land atomically — partial delivery would leave the database or application in an inconsistent state.

## Workflow Mode

**Mode:** `feature-branch`
**Rationale:** Coordinated schema migration (enum type + column + table drop), breaking API changes (code depends on migration, migration breaks existing code), and tightly coupled components require all-or-nothing delivery.
**Label:** `workflow:feature-branch` will be applied to the feature issue TC-9005.

## Inherited Field Propagation

- **Priority:** `High` — inherited from Feature TC-9005 and propagated to all created tasks via `additional_fields: { "priority": {"name": "High"} }`.
- **Fix Versions:** `RHTPA 2.0.0` — inherited from Feature TC-9005 and propagated to all created tasks via `additional_fields: { "fixVersions": [{"name": "RHTPA 2.0.0"}] }`. The `fixVersion scope` configuration defaults to `"both"` (no `### Jira Field Defaults` section is present in CLAUDE.md), so fixVersions are propagated to tasks.
- **Labels:** All created tasks include the `ai-generated-jira` label.
