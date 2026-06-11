# Repository Impact Map — TC-9001

## Feature: Add advisory severity aggregation endpoint

trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model struct to the SBOM model layer
    - Add service method to SbomService that queries the sbom_advisory join table and aggregates advisory severity counts by SBOM ID, deduplicating by advisory ID
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute tower-http cache and optional ?threshold query parameter
    - Add cache invalidation hook in the advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM
    - Add integration tests covering: successful aggregation, 404 for missing SBOM, threshold filtering, cache behavior, and deduplication

## Workflow Mode

**Mode:** direct-to-main

**Rationale:** No atomicity indicators are present. All changes are in a single repository (trustify-backend). The new endpoint is additive — it does not break existing APIs, does not require coordinated schema migrations, and each task can be merged independently without leaving main in a broken state. The model and service can land first, then the endpoint, then cache invalidation, then tests — each PR is self-contained.
