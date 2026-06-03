# Repository Impact Map — TC-9001

## Feature: Add advisory severity aggregation endpoint

### trustify-backend

**Changes:**

- Add `AdvisorySeveritySummary` response model struct with fields: `critical`, `high`, `medium`, `low`, `total`
- Add `advisory_summary` method to `SbomService` that queries the `sbom_advisory` join table, joins to the `advisory` table, deduplicates by advisory ID, and groups counts by severity
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that validates the SBOM exists (returning 404 if not), calls the service method, and returns the severity counts
- Register the new endpoint route in the SBOM endpoints module with 5-minute `tower-http` cache configuration
- Add cache invalidation hook in the advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM
- Support optional `?threshold=critical` query parameter to filter severity counts above a given threshold (non-MVP)
- Add integration tests for the new endpoint covering: successful aggregation, 404 for missing SBOM, deduplication of advisories, cache behavior, and threshold filtering

---

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified. The feature adds a new read-only endpoint without modifying any existing endpoints, database schema, or API contracts. Each task can be merged independently to `main` without leaving the codebase in a broken state:

- The model struct is inert until consumed by the service and endpoint
- The service method is additive and does not modify existing service methods
- The endpoint registration is additive (new route, no changes to existing routes)
- Cache invalidation in the ingestion pipeline is a self-contained hook addition
- Integration tests are fully independent

No coordinated schema migrations, no breaking API changes, no cross-cutting refactors, and no tightly coupled frontend-backend components.
