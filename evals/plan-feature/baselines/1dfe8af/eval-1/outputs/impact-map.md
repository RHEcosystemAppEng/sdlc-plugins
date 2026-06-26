# Repository Impact Map

## Feature: TC-9001 — Add advisory severity aggregation endpoint

trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model in sbom/model/
    - Add advisory_summary service method to SbomService for aggregating severity counts from sbom_advisory join table
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with optional ?threshold query param
    - Register the new advisory-summary route in sbom endpoints/mod.rs
    - Add 5-minute cache layer on the advisory-summary endpoint using tower-http caching middleware
    - Add cache invalidation hook in advisory ingestion pipeline (modules/ingestor/src/graph/advisory/mod.rs)
    - Add integration tests for the new endpoint in tests/api/sbom.rs

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** This feature is self-contained within a single repository (trustify-backend) and involves additive changes only (new endpoint, new model, new service method). No cross-repository coordination or atomicity constraints exist. All tasks can be merged independently to main without risk of partial deployment breaking existing functionality.
