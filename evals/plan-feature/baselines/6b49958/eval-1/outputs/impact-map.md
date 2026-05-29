# Repository Impact Map — TC-9001

## trustify-backend

**Changes:**

- Add `AdvisorySeveritySummary` response model (struct with critical, high, medium, low, total fields)
- Add `AdvisoryService::get_severity_summary(sbom_id)` method to aggregate advisory severity counts using the existing `sbom_advisory` join table
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler with optional `?threshold` query parameter
- Register the new endpoint route in SBOM endpoint module
- Add 5-minute cache configuration to the new endpoint using existing `tower-http` caching middleware
- Add cache invalidation hook in advisory ingestion pipeline when new advisories are linked to an SBOM
- Add integration tests for the new endpoint (success, 404, threshold filter, caching behavior)
- Update API documentation (README.md) with the new endpoint

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators identified. All tasks modify distinct parts of the codebase within a single repository and can be merged independently without leaving `main` in a broken state. There are no coordinated schema migrations, no breaking API changes between tasks, no cross-cutting refactors, and no tightly coupled cross-repo components.
