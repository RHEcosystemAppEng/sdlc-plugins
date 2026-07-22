## Repository
trustify-backend

## Target Branch
main

## Description
Execute smoke tests to validate that the advisory severity aggregation feature works end-to-end. Verify that all new API endpoints return successful responses with valid inputs, that all modified API endpoints maintain backward compatibility, and that the end-to-end workflow (SBOM ingestion, advisory correlation, severity summary retrieval) completes without errors.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns valid JSON with correct severity counts
- [ ] Existing `GET /api/v2/sbom/{id}` and `GET /api/v2/advisory` endpoints are unaffected
- [ ] Advisory ingestion pipeline continues to function correctly with cache invalidation

## Test Requirements
- [ ] Smoke test: call `GET /api/v2/sbom/{id}/advisory-summary` with a valid SBOM ID and verify 200 response
- [ ] Smoke test: call `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` and verify filtered response
- [ ] Smoke test: verify existing SBOM list and detail endpoints still return expected responses
- [ ] Smoke test: ingest a new advisory and verify the end-to-end flow completes successfully

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model
- Depends on: Task 2 — Implement advisory severity aggregation service
- Depends on: Task 3 — Add advisory-summary endpoint with caching
- Depends on: Task 4 — Add cache invalidation on advisory ingestion
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint