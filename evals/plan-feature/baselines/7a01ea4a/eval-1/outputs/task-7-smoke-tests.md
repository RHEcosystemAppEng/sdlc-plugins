## Repository
trustify-backend

## Target Branch
main

## Description
Execute smoke tests for the advisory severity aggregation feature (TC-9001) to verify that the new API endpoint returns successful responses with valid inputs, that existing API endpoints maintain backward compatibility, and that the end-to-end workflow (SBOM ingestion, advisory correlation, summary retrieval) completes without errors. This task validates the testing readiness criteria from the "Smoke Tests" category in the repository's testing readiness template.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with a valid SBOM ID
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with valid parameters
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}` endpoint still returns correct responses (backward compatibility)
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}/advisories` endpoint still returns correct responses (backward compatibility)
- [ ] Smoke test: end-to-end flow — ingest SBOM, correlate advisories, call advisory-summary endpoint — completes without errors

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
- Depends on: Task 3 — Add cache invalidation in advisory ingestion pipeline
- Depends on: Task 4 — Add optional threshold query parameter for severity filtering
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
