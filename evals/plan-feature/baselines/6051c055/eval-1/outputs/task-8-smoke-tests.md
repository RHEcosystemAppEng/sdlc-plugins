## Repository
trustify-backend

## Target Branch
main

## Description
Execute smoke tests to validate that the advisory severity aggregation feature works end-to-end in a deployed environment. Verify that the new GET /api/v2/sbom/{id}/advisory-summary endpoint returns successful responses, that existing SBOM endpoints maintain backward compatibility, and that the complete workflow from advisory ingestion through summary retrieval completes without errors.

## Acceptance Criteria
- [ ] All new endpoints return successful responses
- [ ] Modified endpoints maintain backward compatibility
- [ ] E2E workflow completes — advisory ingestion followed by summary retrieval returns accurate counts

## Test Requirements
- [ ] Smoke test: GET /api/v2/sbom/{id}/advisory-summary returns 200 with valid SBOM ID
- [ ] Smoke test: existing GET /api/v2/sbom endpoints continue to function without regression
- [ ] Smoke test: full workflow — ingest advisory, link to SBOM, retrieve summary — completes successfully

## Dependencies
- Depends on: Task 1 — Advisory severity summary model
- Depends on: Task 2 — Advisory summary service
- Depends on: Task 3 — Advisory summary endpoint
- Depends on: Task 4 — Cache invalidation
- Depends on: Task 5 — Integration tests
- Depends on: Task 6 — Threshold query parameter
