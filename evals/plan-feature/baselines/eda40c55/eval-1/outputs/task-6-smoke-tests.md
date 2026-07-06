## Repository
trustify-backend

## Target Branch
main

## Description
Execute smoke tests to validate that the advisory severity aggregation feature (TC-9001) meets the baseline functional requirements from the testing readiness template. This cross-cutting validation ensures that all new and modified API endpoints return successful responses, maintain backward compatibility, and complete the end-to-end workflow without errors.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Smoke test: GET /api/v2/sbom/{id}/advisory-summary with a valid SBOM ID returns 200 with the expected response shape
- [ ] Smoke test: existing GET /api/v2/sbom/{id} endpoint still works correctly after the changes (backward compatibility)
- [ ] Smoke test: existing GET /api/v2/advisory endpoints still work correctly (backward compatibility)
- [ ] Smoke test: full workflow — ingest SBOM, ingest advisory, correlate, then call advisory-summary — completes without errors

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory ingestion
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
