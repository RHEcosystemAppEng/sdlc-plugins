## Repository
trustify-backend

## Target Branch
main

## Description
Validate the smoke test criteria from the testing readiness template for the advisory severity aggregation feature (TC-9001). This cross-cutting testing task verifies that all new API endpoints return successful responses with valid inputs, all modified API endpoints maintain backward compatibility, and the end-to-end workflow completes without errors.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid SBOM ID and correct JSON shape
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with filtered results
- [ ] Verify existing `GET /api/v2/sbom/{id}` endpoint is unaffected by the new changes
- [ ] Verify existing `GET /api/v2/sbom/{id}/advisories` endpoint is unaffected by the new changes
- [ ] Verify end-to-end workflow: ingest SBOM, ingest advisories, correlate, call advisory-summary endpoint, verify counts

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service
- Depends on: Task 2 — Add advisory summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory severity summary
- Depends on: Task 4 — Add threshold query parameter for advisory summary
- Depends on: Task 5 — Add integration tests for advisory summary endpoint
