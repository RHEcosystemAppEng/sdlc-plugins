# Repository Impact Map

## Feature: TC-9001 — Add advisory severity aggregation endpoint

### trustify-backend

changes:
  - Add `AdvisorySeveritySummary` response model struct with fields: critical, high, medium, low, total
  - Add service method in sbom service to aggregate advisory severity counts for a given SBOM, deduplicating by advisory ID
  - Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint with 404 handling for missing SBOMs and 5-minute cache via tower-http caching middleware
  - Support optional `?threshold` query parameter to filter severity counts above a given level
  - Add cache invalidation hook in the advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM
  - Add integration tests for the new advisory-summary endpoint covering: success response, 404 for unknown SBOM, threshold filtering, deduplication, and cache behavior
  - Update API documentation to include the new endpoint

---

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. All changes target a single repository (trustify-backend). Each task can be merged independently without leaving main in a broken state:
- The model and service layer can land first without any consumer.
- The endpoint can land next, using the service layer already on main.
- Tests can land alongside or after the endpoint.
- Cache invalidation is an additive change to the ingestor that does not break existing behavior if merged independently.

No coordinated schema migrations, no breaking API changes, no cross-cutting refactors, and no tightly coupled cross-repo components.

---

## Summary Comment

**Tasks created:** 5
**Repository affected:** trustify-backend

**Architecture summary:** The implementation adds a new advisory severity aggregation endpoint following the existing module pattern (model + service + endpoints). A new response model (`AdvisorySeveritySummary`) is created in the sbom model directory. The aggregation logic lives in `SbomService`, querying the existing `sbom_advisory` join table and the `advisory` entity to count severities, deduplicating by advisory ID. The endpoint is registered in the sbom endpoints module and mounted via the existing route registration pattern. Cache invalidation is added to the advisory ingestion pipeline. Integration tests follow the existing pattern in `tests/api/`.

**Inherited field values:**
- **Priority:** Major — propagated to all tasks
- **fixVersion:** RHTPA 1.5.0 — propagated to all tasks (fixVersion scope defaults to "both" since no Jira Field Defaults section exists in CLAUDE.md)
