## Repository
trustify-backend

## Target Branch
main

## Description
Execute cross-cutting smoke tests for the advisory severity aggregation feature (TC-9001). Verify that all new and modified API endpoints return successful responses with valid inputs, that existing endpoints maintain backward compatibility, and that the end-to-end workflow from advisory ingestion through advisory-summary query completes without errors.

These tests validate the readiness criteria from the testing readiness template's Smoke Tests category.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with a valid SBOM ID that has correlated advisories
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with filtered counts
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}` endpoint still returns 200 for a valid SBOM (backward compatibility)
- [ ] Smoke test: existing `GET /api/v2/advisory` and `GET /api/v2/advisory/{id}` endpoints still return expected responses (backward compatibility)
- [ ] Smoke test: end-to-end workflow — ingest an SBOM, ingest advisories that correlate to it, then query `GET /api/v2/sbom/{id}/advisory-summary` and verify counts are returned without errors

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory severity summaries
