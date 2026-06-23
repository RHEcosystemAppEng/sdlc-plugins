# Repository Impact Map — TC-9001

## Feature: Add advisory severity aggregation endpoint

### Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. Each task can land on `main` independently without breaking the codebase:
- No coordinated schema migrations (no new tables or columns required)
- No breaking API changes (this is a net-new endpoint; existing endpoints are unchanged)
- No cross-cutting refactors
- Single-repo backend feature with no tightly coupled frontend dependency in scope

---

### trustify-backend

**changes:**
- Add `AdvisorySeveritySummary` response model struct to the SBOM model layer (`modules/fundamental/src/sbom/model/`)
- Add severity aggregation query method to `SbomService` that joins `sbom_advisory` with `advisory` to count advisories by severity, deduplicating by advisory ID
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler with optional `?threshold` query parameter support
- Register the new endpoint route in the SBOM endpoints module
- Add 5-minute `tower-http` cache configuration for the advisory summary endpoint
- Add cache invalidation logic in the advisory ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`) to invalidate cached summaries when new advisories are linked to an SBOM
- Add integration tests for the new endpoint covering: successful aggregation, 404 for missing SBOM, response shape validation, threshold query parameter filtering, and cache behavior
- Update API documentation (README.md) to document the new endpoint
