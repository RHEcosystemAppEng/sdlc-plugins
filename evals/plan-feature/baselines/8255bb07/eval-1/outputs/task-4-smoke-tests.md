## Repository
trustify-backend

## Target Branch
main

## Description
Execute smoke tests for the advisory severity aggregation feature (TC-9001) to validate that all new and modified API endpoints return successful responses and that the end-to-end workflow completes without errors. This cross-cutting testing task verifies feature-level readiness per the testing readiness template's Smoke Tests category.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Verify GET /api/v2/sbom/{id}/advisory-summary returns 200 with valid SBOM ID and correctly shaped response body
- [ ] Verify GET /api/v2/sbom/{id}/advisory-summary returns 404 with non-existent SBOM ID
- [ ] Verify GET /api/v2/sbom/{id}/advisory-summary?threshold=critical returns 200 with filtered severity counts
- [ ] Verify existing SBOM endpoints (GET /api/v2/sbom, GET /api/v2/sbom/{id}) continue to function without regression after the changes
- [ ] Verify end-to-end flow: ingest SBOM, ingest advisory, correlate advisory to SBOM, call advisory-summary endpoint, confirm counts are correct

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching and threshold filter
- Depends on: Task 3 — Add cache invalidation for advisory summaries on advisory ingestion
