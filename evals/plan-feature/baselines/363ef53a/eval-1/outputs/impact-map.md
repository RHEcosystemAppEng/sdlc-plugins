# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## Workflow Mode

**Mode:** direct-to-main

**Rationale:** No atomicity indicators identified. This feature adds a new endpoint within a single repository (trustify-backend) with no coordinated schema migrations, no breaking API changes (the endpoint is additive), no cross-cutting refactors, and no tightly coupled frontend-backend components. All tasks can be merged independently to main without leaving the codebase in a broken state.

## Inherited Field Values

- **Priority:** Major (inherited from Feature TC-9001)
- **fixVersions:** RHTPA 1.5.0 (inherited from Feature TC-9001; no `fixVersion scope` setting in Jira Field Defaults — defaulting to "both", propagated to tasks)

## Changes

trustify-backend:
  changes:
    - Add AdvisorySeveritySummary model struct with severity count fields (critical, high, medium, low, total)
    - Add aggregation service method to SbomService that counts unique advisories per severity for a given SBOM
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache and optional threshold query parameter
    - Add cache invalidation in the advisory ingestion pipeline when new advisories are linked to an SBOM
    - Add integration tests for the advisory-summary endpoint covering happy path, 404, threshold filter, and deduplication
    - Update REST API reference documentation to include the new endpoint

## Excluded Requirements

| Requirement | Reason for Exclusion |
|---|---|
| Add the new endpoint to the API latency Grafana dashboard | Operational/infrastructure concern — no monitoring or Grafana repository is present in the Repository Registry. Requires a separate infrastructure task outside this feature's scope. |
| Alert if p95 exceeds 500ms | Operational/infrastructure concern — alerting configuration is outside the scope of the trustify-backend repository. Requires a separate infrastructure task. |

## Task Summary

| # | Summary | Repository | Dependencies |
|---|---|---|---|
| 1 | Add advisory severity summary model and aggregation service method | trustify-backend | None |
| 2 | Add advisory-summary endpoint with caching | trustify-backend | Task 1 |
| 3 | Add cache invalidation for advisory summaries during advisory ingestion | trustify-backend | Task 2 |
| 4 | Add integration tests for advisory-summary endpoint | trustify-backend | Task 2 |
| 5 | Update REST API reference documentation | trustify-backend | Tasks 1, 2, 3, 4 |
| 6 | Smoke Tests | trustify-backend | Tasks 1, 2, 3, 4 |
| 7 | Performance Benchmarks | trustify-backend | Tasks 1, 2, 3, 4 |
