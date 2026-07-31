## Repository
trustify-backend

## Target Branch
main

## Priority
Major

## Fix Versions
RHTPA 1.5.0

## Description
Execute smoke tests for the advisory severity aggregation endpoint feature (TC-9001). Validate that all new and modified API endpoints return successful responses with valid inputs, maintain backward compatibility for existing endpoints, and that the end-to-end workflow completes without errors.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid SBOM ID
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 404 with invalid SBOM ID
- [ ] Existing `GET /api/v2/sbom/{id}` endpoint still works correctly after changes
- [ ] Advisory ingestion pipeline still completes successfully after cache invalidation changes

## Test Requirements
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Dependencies
- Depends on: Task 1 — Create advisory severity summary model
- Depends on: Task 2 — Implement advisory severity aggregation service method
- Depends on: Task 3 — Add advisory-summary endpoint with caching
- Depends on: Task 4 — Add cache invalidation for advisory summary on ingestion
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
