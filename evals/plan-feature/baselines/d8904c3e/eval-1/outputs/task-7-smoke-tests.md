## Repository
trustify-backend

## Target Branch
main

## Description
Execute cross-cutting smoke tests to validate that the advisory severity aggregation feature (TC-9001) is functional end-to-end. This testing task covers the Smoke Tests category from the testing readiness template, verifying that all new and modified API endpoints return successful responses and that the end-to-end workflow (SBOM ingestion, advisory correlation, severity summary retrieval) completes without errors.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid SBOM ID and correct JSON shape
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with filtered counts
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}` endpoint still returns expected responses (backward compatibility)
- [ ] Smoke test: existing `GET /api/v2/advisory` endpoint still returns expected responses (backward compatibility)
- [ ] Smoke test: end-to-end workflow — ingest SBOM, ingest advisory, correlate, call advisory-summary, verify counts reflect the correlation

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and service method
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
- Depends on: Task 3 — Add cache invalidation in advisory ingestion pipeline
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
- Depends on: Task 5 — Add optional threshold query parameter support
