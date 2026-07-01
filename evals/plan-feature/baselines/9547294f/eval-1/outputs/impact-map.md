# Repository Impact Map — TC-9001

## Feature: Add advisory severity aggregation endpoint

### trustify-backend

**Changes:**

- Add `AdvisorySeveritySummary` response model struct with fields `critical`, `high`, `medium`, `low`, `total` in the SBOM model layer
- Add service method on `SbomService` to query the `sbom_advisory` join table, join to `advisory` for severity, deduplicate by advisory ID, and aggregate counts by severity level
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler in the SBOM endpoints module with 5-minute cache configuration via tower-http caching middleware
- Return 404 (consistent with existing SBOM endpoints) when the SBOM ID does not exist
- Add optional `?threshold` query parameter support to filter severity counts above a given severity level (non-MVP)
- Add cache invalidation hook in the advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM
- Add integration tests for the new endpoint covering: success with severity counts, 404 for missing SBOM, cache behavior, and threshold filtering
- Update API documentation to include the new endpoint path, parameters, and response shape

---

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified. All changes are within a single repository (trustify-backend). The new endpoint does not modify existing API contracts or database schema — it adds a new read-only aggregation endpoint using existing tables (`sbom_advisory`, `advisory`). No coordinated schema migrations, no breaking API changes, no cross-cutting refactors, and no tightly coupled cross-repo components. Each task can be merged independently to `main` without leaving the codebase in a broken state.
