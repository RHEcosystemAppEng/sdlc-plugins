## Repository
trustify-backend

## Target Branch
main

## Description
Perform smoke testing for the advisory severity aggregation feature (TC-9001). Validate that the new API endpoint returns successful responses with valid inputs, that existing SBOM and advisory endpoints maintain backward compatibility, and that the end-to-end workflow (SBOM ingestion, advisory correlation, summary retrieval) completes without errors.

This testing task covers the "Smoke Tests" category from the testing readiness template at `docs/testing-readiness.md`.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid JSON for an existing SBOM with correlated advisories
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with valid JSON
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}` endpoint still returns expected responses (backward compatibility)
- [ ] Smoke test: existing `GET /api/v2/advisory` endpoint still returns expected responses (backward compatibility)
- [ ] Smoke test: ingest an SBOM, ingest advisories, correlate them, then call `GET /api/v2/sbom/{id}/advisory-summary` and verify the complete end-to-end workflow returns correct severity counts

## Dependencies
- Depends on: Task 1 — Add severity aggregation model and service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summaries
- Depends on: Task 4 — Add threshold query parameter support
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
