# TC-9001: Add advisory severity aggregation endpoint — Implementation Plan

## Tasks

| # | Task | Repository | Dependencies |
|---|------|------------|-------------|
| 1 | Define AdvisorySeveritySummary response model | trustify-backend | — |
| 2 | Implement advisory severity aggregation service method | trustify-backend | Task 1 |
| 3 | Add GET /api/v2/sbom/{id}/advisory-summary endpoint | trustify-backend | Task 2 |
| 4 | Add cache invalidation on advisory ingestion | trustify-backend | Task 3 |
| 5 | Add integration tests for advisory summary endpoint | trustify-backend | Task 3, Task 4 |
| 6 | Mount advisory summary route in server and update API documentation | trustify-backend | Task 3 |

## Repositories Affected

- **trustify-backend** — sole repository; all 6 tasks target this repo

## Architecture Summary

This feature adds a new `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint to the trustify-backend service. The implementation follows the existing domain module pattern (`model/ + service/ + endpoints/`):

1. **Model layer** (Task 1): A new `AdvisorySeveritySummary` struct in the SBOM module captures aggregated severity counts (critical, high, medium, low, total).

2. **Service layer** (Task 2): A new method on `SbomService` queries the `sbom_advisory` join table, deduplicates by advisory ID, and aggregates counts by severity level. Supports an optional threshold filter for severity-level filtering.

3. **Endpoint layer** (Task 3): An Axum handler extracts the SBOM ID from the path and an optional `?threshold` query parameter, delegates to the service, and returns the JSON response. The route is configured with 5-minute `tower-http` caching.

4. **Cache invalidation** (Task 4): The advisory ingestion pipeline in the ingestor module is extended to invalidate cached summary responses when new advisories are linked to an SBOM.

5. **Testing** (Task 5): Comprehensive integration tests in `tests/api/` cover the happy path, empty results, deduplication, 404 errors, and threshold filtering.

6. **Server wiring** (Task 6): Verification that the new route is properly mounted in `server/main.rs` and accessible at runtime.

**Workflow mode**: Direct-to-main. Single repository, no cross-repo atomicity constraints. All tasks target the `main` branch.

**No new database tables** are required — the feature uses the existing `sbom_advisory` join table and `advisory` entity.

Inherited fields propagated to tasks: priority=Major, fixVersion=RHTPA 1.5.0
