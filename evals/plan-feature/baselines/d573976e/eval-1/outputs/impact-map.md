# Repository Impact Map

**Feature:** TC-9001 — Add advisory severity aggregation endpoint
**Workflow Mode:** direct-to-main

## trustify-backend

changes:
  - Add `AdvisorySeveritySummary` response model struct to `modules/fundamental/src/sbom/model/`
  - Add aggregation query method to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` that joins `sbom_advisory` with `advisory` entities, groups by severity, and returns deduplicated counts
  - Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler in `modules/fundamental/src/sbom/endpoints/`
  - Register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` with 5-minute cache configuration
  - Add optional `?threshold` query parameter support to filter severity counts (non-MVP)
  - Add cache invalidation hook in advisory ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`) to invalidate cached summaries when new advisories are linked to an SBOM
  - Add integration tests for the new endpoint in `tests/api/`
  - Update API documentation to include the new endpoint

## Rationale — Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:
- No coordinated schema migrations: the feature explicitly requires no new database tables and uses existing advisory-SBOM relationship tables
- No breaking API changes: the endpoint is purely additive (new GET endpoint)
- No cross-cutting refactors: changes are contained within the existing module pattern
- No tightly coupled cross-repo components: all changes are in a single repository (trustify-backend)

All tasks can be merged independently to `main` without leaving the codebase in a broken state.
