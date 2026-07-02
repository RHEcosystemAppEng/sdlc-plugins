# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## Workflow Mode

**Mode:** direct-to-main

**Rationale:** No atomicity indicators were identified. The feature adds a new REST endpoint
without modifying existing API contracts, without requiring database schema migrations, and
without cross-cutting refactors. Each task can be merged to main independently without leaving
the codebase in a broken state.

## Impact Map

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model struct in modules/fundamental/src/sbom/model/
    - Add severity aggregation query method to SbomService that counts advisories by severity with deduplication by advisory ID
    - Create GET /api/v2/sbom/{id}/advisory-summary endpoint handler with 5-minute cache TTL via tower-http caching middleware
    - Register new advisory-summary route in modules/fundamental/src/sbom/endpoints/mod.rs
    - Add cache invalidation for advisory-summary in advisory ingestion pipeline (modules/ingestor/src/graph/advisory/mod.rs)
    - Add integration tests for advisory-summary endpoint in tests/api/sbom.rs (happy path, 404, deduplication, empty case)
    - Add optional ?threshold query parameter for severity filtering on the advisory-summary endpoint
```

## Priority/fixVersions Propagation

- **Priority**: Major (inherited from TC-9001, propagated to all created tasks)
- **Fix Versions**: RHTPA 1.5.0 (inherited from TC-9001, propagated to all created tasks; fixVersion scope defaults to "both" since no Jira Field Defaults section exists in CLAUDE.md)

All tasks will include the following additional_fields when created in Jira:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

## Task Summary

| # | Task | Repository | Dependencies |
|---|---|---|---|
| 1 | Add AdvisorySeveritySummary model and severity aggregation service method | trustify-backend | None |
| 2 | Create GET /api/v2/sbom/{id}/advisory-summary endpoint with caching | trustify-backend | Task 1 |
| 3 | Add cache invalidation for advisory summaries during advisory ingestion | trustify-backend | Task 2 |
| 4 | Add integration tests for advisory-summary endpoint | trustify-backend | Task 2 |
| 5 | Add optional threshold query parameter for severity filtering | trustify-backend | Task 2 |

## Architecture Summary

The feature adds a server-side advisory severity aggregation endpoint to the existing SBOM
module following the established model/service/endpoints module pattern. The new endpoint
queries the existing `sbom_advisory` join table and `advisory` entity to produce deduplicated
severity counts, eliminating the need for clients to fetch and count advisories page by page.
Caching is handled via the existing tower-http caching middleware with a 5-minute TTL, and
the advisory ingestion pipeline is extended to invalidate cached summaries when new
advisory-SBOM correlations are created. No new database tables or migrations are required.
