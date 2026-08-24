## Repository
trustify-backend

## Target Branch
main

## Description
Perform smoke testing for the TC-9001 advisory severity aggregation feature. Validate that all new and modified API endpoints return successful responses with valid inputs, maintain backward compatibility on existing endpoints, and that the end-to-end workflow (SBOM ingestion, advisory correlation, advisory-summary retrieval) completes without errors. This testing task covers the Smoke Tests category from the project's testing readiness template.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Call `GET /api/v2/sbom/{id}/advisory-summary` with a valid SBOM ID that has linked advisories and verify a 200 response with the expected JSON structure
- [ ] Call `GET /api/v2/sbom/{id}/advisory-summary` with the optional `?threshold` parameter and verify correct filtered response
- [ ] Verify that existing SBOM endpoints (`GET /api/v2/sbom`, `GET /api/v2/sbom/{id}`) still function correctly after the changes
- [ ] Verify that existing advisory endpoints (`GET /api/v2/advisory`, `GET /api/v2/advisory/{id}`) still function correctly after the changes
- [ ] Execute end-to-end workflow: ingest SBOM, ingest advisories, correlate, call advisory-summary, verify counts reflect ingested data

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summary on advisory ingestion
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
