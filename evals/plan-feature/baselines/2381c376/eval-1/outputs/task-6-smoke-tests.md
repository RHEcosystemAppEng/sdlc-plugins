## Repository
trustify-backend

## Target Branch
main

## Description
Execute smoke tests for the advisory severity aggregation feature (TC-9001) to validate that all new and modified API endpoints return successful responses with valid inputs, maintain backward compatibility on modified endpoints, and that the end-to-end workflow completes without errors. This testing task covers the Smoke Tests category from the testing readiness template.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with a valid SBOM ID that has linked advisories
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with correct filtered response
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for a nonexistent SBOM ID
- [ ] Verify existing SBOM endpoints (`GET /api/v2/sbom`, `GET /api/v2/sbom/{id}`) still return expected responses after changes (backward compatibility)
- [ ] Verify existing advisory endpoints (`GET /api/v2/advisory`, `GET /api/v2/advisory/{id}`) still return expected responses after changes
- [ ] Verify end-to-end workflow: ingest SBOM, ingest advisories, call advisory-summary endpoint, receive correct severity counts

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching and threshold filter
- Depends on: Task 3 — Add cache invalidation in advisory ingestion pipeline
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
