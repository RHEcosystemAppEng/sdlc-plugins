# Task 7 — Smoke Tests for advisory severity aggregation feature

## Repository
trustify-backend

## Target Branch
main

## Description
Execute cross-cutting smoke tests to validate the advisory severity aggregation feature at the feature level. This testing task covers the Smoke Tests category from the testing readiness template, verifying that all new API endpoints return successful responses with valid inputs, all modified API endpoints maintain backward compatibility, and the end-to-end workflow completes without errors.

Reference: Feature TC-9001 — Add advisory severity aggregation endpoint.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid SBOM ID and correct JSON response shape
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with filtered counts
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}` endpoint still returns correct responses (backward compatibility)
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}/advisories` endpoint still returns correct responses (backward compatibility)
- [ ] Smoke test: end-to-end flow — ingest SBOM, ingest advisories, correlate, call advisory-summary — completes without errors

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and severity aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Add threshold query parameter to advisory-summary endpoint
- Depends on: Task 4 — Add cache invalidation for advisory-summary on advisory ingestion
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
