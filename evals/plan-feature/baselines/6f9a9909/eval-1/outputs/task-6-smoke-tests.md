## Repository
trustify-backend

## Target Branch
main

## Description
Execute smoke tests for the advisory severity aggregation feature (TC-9001) to verify that all new and modified API endpoints function correctly with valid inputs, maintain backward compatibility, and that the end-to-end workflow completes without errors. This is a cross-cutting validation activity derived from the testing readiness template's Smoke Tests category.

The smoke tests should verify:
- The new `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns successful responses with valid inputs
- Existing SBOM and advisory endpoints (`GET /api/v2/sbom/{id}`, `GET /api/v2/advisory`) continue to work correctly after the changes
- The end-to-end workflow (ingest SBOM, ingest advisories, query advisory-summary) completes without errors

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid SBOM ID
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary` returns valid JSON with expected field names
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}` endpoint still returns correct responses (backward compatibility)
- [ ] Smoke test: existing `GET /api/v2/advisory` endpoint still returns correct responses (backward compatibility)
- [ ] Smoke test: full workflow — ingest SBOM, ingest advisory, call advisory-summary — returns correct severity counts

## Dependencies
- Depends on: Task 1 — Create AdvisorySeveritySummary model and aggregation service
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation on advisory ingestion
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
