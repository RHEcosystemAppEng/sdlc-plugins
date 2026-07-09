## Repository
trustify-backend

## Target Branch
main

## Description
Execute smoke tests for the advisory severity aggregation feature (TC-9001) to validate that all new and modified API endpoints return successful responses and that the end-to-end workflow completes without errors. This testing task covers the "Smoke Tests" category from the testing readiness template.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid inputs
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with valid inputs
- [ ] Verify existing SBOM endpoints (`GET /api/v2/sbom/{id}`, `GET /api/v2/sbom`) still work correctly after changes
- [ ] Verify existing advisory endpoints (`GET /api/v2/advisory`, `GET /api/v2/advisory/{id}`) still work correctly
- [ ] Verify end-to-end flow: ingest SBOM, ingest advisory, correlate, call advisory-summary endpoint, verify response

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summaries
- Depends on: Task 4 — Add threshold query parameter support
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
