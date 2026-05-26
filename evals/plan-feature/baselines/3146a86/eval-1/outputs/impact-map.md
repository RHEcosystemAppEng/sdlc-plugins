# Repository Impact Map -- TC-9001: Add advisory severity aggregation endpoint

## Workflow Mode: `direct-to-main`

**Rationale:** No atomicity indicators are present. The feature adds a new endpoint
that does not break existing endpoints or require coordinated schema migrations. The
new `GET /api/v2/sbom/{id}/advisory-summary` endpoint is additive -- existing clients
are unaffected. No cross-cutting refactors are needed, and no existing API contracts
change. All tasks can be merged independently to `main` without leaving the codebase
in a broken state.

---

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary model struct with fields: critical, high, medium, low, total
    - Add service method to SbomService that queries sbom_advisory join table, joins advisory table, groups by severity, deduplicates by advisory ID, and returns aggregated counts
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 404 handling for missing SBOMs
    - Add 5-minute cache configuration to the advisory-summary endpoint route using tower-http caching middleware
    - Add optional ?threshold query parameter to filter severity counts above a given level
    - Add cache invalidation hook in advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM
    - Add integration tests for the advisory-summary endpoint covering: success with counts, 404 for missing SBOM, threshold filtering, deduplication of advisory IDs, and cache behavior
    - Update API documentation to include the new endpoint
```
