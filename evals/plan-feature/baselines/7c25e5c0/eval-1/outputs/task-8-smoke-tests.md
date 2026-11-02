## Repository
trustify-backend

## Target Branch
main

## Description
Execute cross-cutting smoke tests for the TC-9001 advisory severity aggregation feature. Validate that all new and modified API endpoints return successful responses with valid inputs, maintain backward compatibility, and that the end-to-end workflow completes without errors. These tests verify the feature at a higher level than unit or integration tests, ensuring the complete advisory summary flow works correctly from ingestion through API response.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid SBOM ID and correct JSON shape
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with filtered results
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}` endpoint still returns 200 (backward compatibility)
- [ ] Smoke test: existing `GET /api/v2/advisory` endpoint still returns 200 (backward compatibility)
- [ ] Smoke test: ingest an advisory, verify advisory summary updates reflect the new data (end-to-end)

## Dependencies
- Depends on: Task 1 — Advisory severity summary model
- Depends on: Task 2 — Advisory summary aggregation service
- Depends on: Task 3 — Advisory summary endpoint with caching
- Depends on: Task 4 — Cache invalidation on advisory ingestion
- Depends on: Task 5 — Threshold query parameter filter
- Depends on: Task 6 — Integration tests for advisory summary
