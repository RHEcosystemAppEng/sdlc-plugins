# Repository Impact Map -- TC-9001

## Feature: Add advisory severity aggregation endpoint

### trustify-backend

**Changes:**
- Add `AdvisorySeveritySummary` response model struct with fields `critical`, `high`, `medium`, `low`, `total`
- Add `get_advisory_summary` method to `SbomService` that queries the `sbom_advisory` join table, joins to advisory to read severity, deduplicates by advisory ID, and aggregates counts by severity level
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that calls the new service method, returns 404 if SBOM not found, and applies 5-minute `tower-http` cache
- Support optional `?threshold=critical` query parameter to filter severity counts above a threshold (non-MVP)
- Add cache invalidation hook in the advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM
- Add integration tests for the new endpoint covering: success with severity counts, 404 for nonexistent SBOM, cache behavior, and threshold filtering
- Update API documentation to include the new endpoint

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. This feature is entirely additive within a single repository -- it adds a new endpoint without modifying existing API contracts, database schema, or cross-repository dependencies. Each task can be merged independently to `main` without leaving the codebase in a broken state.
