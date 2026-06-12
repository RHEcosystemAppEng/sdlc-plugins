# Repository Impact Map — TC-9001

## trustify-backend

### Workflow Mode: `direct-to-main`

**Rationale:** No atomicity indicators identified. All tasks can be merged independently without leaving `main` in a broken state:
- No coordinated schema migrations (no new database tables required per NFRs)
- No breaking API changes (this is a new additive endpoint; existing endpoints are unchanged)
- No cross-cutting refactors (changes are scoped to the SBOM/advisory domain)
- No tightly coupled feature components (single backend repository; no frontend changes required)

### Changes

1. **Add `AdvisorySeveritySummary` response model** — Create a new struct representing the severity aggregation response (`critical`, `high`, `medium`, `low`, `total` fields) in the SBOM model layer, following the existing `SbomSummary`/`SbomDetails` pattern.

2. **Add advisory severity aggregation query to `SbomService`** — Implement a service method that queries the `sbom_advisory` join table joined with the `advisory` table, deduplicates by advisory ID, groups by severity, and returns counts as an `AdvisorySeveritySummary`. Support the optional `threshold` query parameter for severity filtering.

3. **Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint** — Register a new endpoint handler under the SBOM endpoint module that validates the SBOM ID exists (returning 404 if not), calls the service method, applies 5-minute cache headers via `tower-http` caching middleware, and returns the `AdvisorySeveritySummary` response.

4. **Add cache invalidation for advisory summary on advisory ingestion** — Modify the advisory ingestion pipeline to invalidate cached advisory summaries when new advisories are linked to an SBOM, ensuring stale data is not served.

5. **Add integration tests for the advisory-summary endpoint** — Create integration tests covering: successful aggregation with deduplication, 404 for non-existent SBOM, threshold query parameter filtering, empty advisory set, and cache behavior verification.

6. **Update REST API documentation** — Add the new endpoint to the API reference documentation, including path, parameters, response shape, and examples.
