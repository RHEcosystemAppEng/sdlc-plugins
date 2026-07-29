## Repository
trustify-backend

## Target Branch
main

## Description
Execute smoke tests for the advisory severity aggregation feature (TC-9001) to validate that all new and modified API endpoints return successful responses with valid inputs, maintain backward compatibility with existing endpoints, and that the end-to-end workflow completes without errors. This is a cross-cutting validation activity based on the testing readiness template at `docs/testing-readiness.md`.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid SBOM ID and correct JSON shape
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with valid parameters
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}` endpoint continues to return 200 (backward compatibility)
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}/advisories` endpoint continues to return 200 (backward compatibility)
- [ ] Smoke test: end-to-end workflow — ingest SBOM, ingest advisories, call advisory-summary endpoint — completes without errors

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service layer
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation in advisory ingestion pipeline
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
- Depends on: Task 5 — Add optional threshold query parameter
