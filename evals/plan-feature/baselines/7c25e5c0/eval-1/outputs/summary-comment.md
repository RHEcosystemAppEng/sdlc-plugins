# Plan Summary — TC-9001: Add advisory severity aggregation endpoint

## Tasks Created

| # | Summary | Repository | Type |
|---|---------|------------|------|
| 1 | Advisory severity summary model | trustify-backend | Implementation |
| 2 | Advisory summary aggregation service | trustify-backend | Implementation |
| 3 | Advisory summary endpoint with caching | trustify-backend | Implementation |
| 4 | Cache invalidation on advisory ingestion | trustify-backend | Implementation |
| 5 | Threshold query parameter filter | trustify-backend | Implementation |
| 6 | Integration tests for advisory summary | trustify-backend | Implementation |
| 7 | Documentation — REST API reference | trustify-backend | Documentation |
| 8 | Smoke Tests | trustify-backend | Testing |
| 9 | Performance Benchmarks | trustify-backend | Testing |

## Repositories Affected

- **trustify-backend** — all changes target this repository

## Architecture Summary

The feature adds a server-side advisory severity aggregation endpoint (`GET /api/v2/sbom/{id}/advisory-summary`) to replace client-side counting. The implementation follows the existing module pattern (model → service → endpoint) and integrates with the advisory ingestion pipeline for cache invalidation. An optional threshold query parameter enables alerting integrations to filter by severity level.

## Inherited Field Propagation

- **Priority:** `Major` — inherited from TC-9001 and propagated to all 9 created tasks. The Feature's priority was set (not "Undefined"), so it was included in `additional_fields.priority` for each task.
- **fixVersions:** `RHTPA 1.5.0` — inherited from TC-9001 and propagated to all 9 created tasks. The Feature has a non-empty fixVersions array, and the fixVersion scope configuration defaults to `both` (no explicit override in Jira Field Defaults), so task-level propagation applies. Included in `additional_fields.fixVersions` for each task.
