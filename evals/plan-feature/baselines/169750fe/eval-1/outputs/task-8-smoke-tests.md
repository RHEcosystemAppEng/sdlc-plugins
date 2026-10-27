## Repository
trustify-backend

## Target Branch
main

## Description
Execute cross-cutting smoke tests for Feature TC-9001 (advisory severity aggregation endpoint) to validate that the feature works end-to-end. This testing task covers the Smoke Tests category from the testing readiness template, verifying that all new and modified API endpoints respond correctly with valid inputs and that the end-to-end workflow completes without errors.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid SBOM ID and correct severity count JSON shape
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with filtered counts
- [ ] Verify existing `GET /api/v2/sbom/{id}` and `GET /api/v2/advisory` endpoints are unaffected by the changes
- [ ] Verify the full workflow: ingest SBOM, correlate advisories, call advisory-summary endpoint, verify counts match expected values
- [ ] Verify cache invalidation: ingest a new advisory after initial summary call, verify updated counts on subsequent request

## Dependencies
- Depends on: Task 1 — Advisory severity summary model
- Depends on: Task 2 — Advisory summary service
- Depends on: Task 3 — Advisory summary endpoint
- Depends on: Task 4 — Cache invalidation
- Depends on: Task 5 — Integration tests
- Depends on: Task 6 — Threshold query param
