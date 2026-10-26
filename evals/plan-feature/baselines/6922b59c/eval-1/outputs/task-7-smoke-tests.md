## Repository
trustify-backend

## Target Branch
main

## Description
Execute smoke tests for the advisory severity aggregation feature (TC-9001) to validate that new and modified API endpoints return successful responses with valid inputs, maintain backward compatibility, and complete the end-to-end workflow without errors. This testing task covers the Smoke Tests category from the testing readiness template.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with a valid SBOM ID that has linked advisories
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for a non-existent SBOM ID
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with filtered counts
- [ ] Verify existing `GET /api/v2/sbom/{id}` endpoint is unaffected by the new changes
- [ ] Verify existing `GET /api/v2/advisory` endpoint is unaffected by the new changes
- [ ] Verify advisory ingestion pipeline completes without errors after cache invalidation changes
- [ ] Verify the complete workflow: ingest SBOM, ingest advisory, correlate, then call advisory-summary endpoint and receive correct counts

## Dependencies
- Depends on: Task 1 — Add advisory severity summary response model
- Depends on: Task 2 — Add SBOM advisory severity aggregation service method
- Depends on: Task 3 — Add advisory summary REST endpoint with caching
- Depends on: Task 4 — Add cache invalidation on advisory ingestion
- Depends on: Task 5 — Add integration tests for advisory summary endpoint
