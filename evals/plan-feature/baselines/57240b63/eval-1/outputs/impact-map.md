# Repository Impact Map — TC-9001

## Feature: Add advisory severity aggregation endpoint

### Workflow Mode: direct-to-main

**Rationale:** No atomicity indicators are present. This feature adds a new endpoint
to a single repository with no coordinated schema migrations (no new tables), no
breaking API changes (new endpoint only), no cross-cutting refactors, and no tightly
coupled cross-repo components. Each task can be merged to `main` independently without
leaving the codebase in a broken state.

---

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model struct to the sbom module (modules/fundamental/src/sbom/model/)
    - Add advisory severity aggregation query method to SbomService using the sbom_advisory join table and advisory severity field (modules/fundamental/src/sbom/service/sbom.rs)
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache TTL via tower-http caching middleware (modules/fundamental/src/sbom/endpoints/)
    - Add optional ?threshold query parameter to filter severity counts above a given level (modules/fundamental/src/sbom/endpoints/)
    - Add cache invalidation for advisory summaries in the advisory ingestion pipeline when new advisories are linked to an SBOM (modules/ingestor/src/graph/advisory/mod.rs)
    - Add integration tests for the advisory summary endpoint covering happy path, 404, caching, threshold filtering, and deduplication (tests/api/)
```

### Inherited Jira Fields

- **Priority:** Major (propagated from Feature TC-9001)
- **Fix Versions:** RHTPA 1.5.0 (propagated from Feature TC-9001; fixVersion scope: both)
