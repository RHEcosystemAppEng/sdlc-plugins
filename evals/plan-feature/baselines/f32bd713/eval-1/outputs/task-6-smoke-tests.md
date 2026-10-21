## Repository
trustify-backend

## Target Branch
main

## Description
Execute cross-cutting smoke tests to validate that the advisory severity aggregation feature (TC-9001) works end-to-end after all implementation tasks are complete. This testing task covers the Smoke Tests category from the testing readiness template, verifying that all new and modified API endpoints return successful responses with valid inputs, maintain backward compatibility, and that the end-to-end workflow completes without errors.

Ref: TC-9001

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Smoke test: call GET /api/v2/sbom/{id}/advisory-summary with valid SBOM ID and verify 200 response with correct JSON shape
- [ ] Smoke test: call GET /api/v2/sbom/{id}/advisory-summary?threshold=critical and verify 200 response with filtered counts
- [ ] Smoke test: verify existing GET /api/v2/sbom/{id} endpoint still returns expected responses (backward compatibility)
- [ ] Smoke test: verify existing GET /api/v2/advisory endpoints still return expected responses (backward compatibility)
- [ ] Smoke test: end-to-end workflow -- ingest an SBOM, ingest advisories, call advisory-summary endpoint, verify correct severity counts

## Dependencies
- Depends on: Task 1 -- Add AdvisorySeveritySummary model and aggregation service method
- Depends on: Task 2 -- Add advisory-summary endpoint with caching
- Depends on: Task 3 -- Add cache invalidation for advisory summaries
- Depends on: Task 4 -- Add threshold query parameter filtering
