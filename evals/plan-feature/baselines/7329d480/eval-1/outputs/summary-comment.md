## Planning Complete — TC-9001: Add advisory severity aggregation endpoint

### Tasks Created

| # | Task | Repository | Dependencies |
|---|---|---|---|
| 1 | Define advisory severity summary response model | trustify-backend | None |
| 2 | Implement advisory severity aggregation query in SbomService | trustify-backend | Task 1 |
| 3 | Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching | trustify-backend | Task 2 |
| 4 | Invalidate advisory summary cache on advisory ingestion | trustify-backend | Task 3 |
| 5 | Integration tests for advisory summary endpoint | trustify-backend | Task 3 |
| 6 | Update REST API reference documentation | trustify-backend | Task 3, Task 5 |

### Repositories Affected

- **trustify-backend** (sole repository) — direct-to-main workflow, no feature branch needed

### Architecture Summary

The implementation adds a new `GET /api/v2/sbom/{id}/advisory-summary` endpoint following the existing module pattern (`model/ + service/ + endpoints/`). A new `AdvisorySeveritySummary` response model is defined, a service method performs a `GROUP BY severity` aggregation query against the `sbom_advisory` join table with deduplication by advisory ID, and an Axum handler exposes it as a cached endpoint with 5-minute TTL. Cache invalidation is wired into the advisory ingestion pipeline so newly correlated advisories are reflected immediately. Comprehensive integration tests and documentation round out the feature.

### Inherited Field Values

- **Priority**: Major -- propagated from TC-9001 to all tasks
- **Fix Versions**: RHTPA 1.5.0 -- propagated from TC-9001 to all tasks
