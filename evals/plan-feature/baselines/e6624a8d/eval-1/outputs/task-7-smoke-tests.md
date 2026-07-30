## Repository
trustify-backend

## Target Branch
main

## Description
Execute cross-cutting smoke tests for the advisory severity aggregation feature (TC-9001). These tests validate that the new API endpoint returns successful responses with valid inputs, that existing SBOM and advisory endpoints maintain backward compatibility, and that the end-to-end workflow (ingest SBOM, correlate advisories, query summary) completes without errors.

Test category: Smoke Tests (from testing readiness template).

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid SBOM ID
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with valid inputs
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}` endpoint still returns expected responses (backward compatibility)
- [ ] Smoke test: existing `GET /api/v2/advisory` endpoint still returns expected responses (backward compatibility)
- [ ] Smoke test: ingest an SBOM, correlate advisories, then call advisory-summary — full workflow completes without errors

## Dependencies
- Depends on: Task 1 — Add advisory severity summary response model
- Depends on: Task 2 — Add advisory severity aggregation service method
- Depends on: Task 3 — Add advisory-summary REST endpoint with caching
- Depends on: Task 4 — Add cache invalidation for advisory ingestion
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
