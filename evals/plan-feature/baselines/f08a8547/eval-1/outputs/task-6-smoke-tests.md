## Repository
trustify-backend

## Target Branch
main

## Description
Execute smoke tests for the advisory severity aggregation feature (TC-9001) to verify that all new and modified API endpoints function correctly with valid inputs, maintain backward compatibility, and complete the end-to-end workflow without errors. This task validates the cross-cutting smoke test criteria from the testing readiness template.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary` returns a successful response (200) with valid SBOM ID and correctly shaped JSON body
- [ ] Verify existing `GET /api/v2/sbom/{id}` endpoint continues to function correctly after the changes (backward compatibility)
- [ ] Verify existing `GET /api/v2/advisory` and `GET /api/v2/advisory/{id}` endpoints continue to function correctly (backward compatibility)
- [ ] Verify the end-to-end workflow: ingest an SBOM, ingest advisories, correlate them, then call `advisory-summary` and confirm correct severity counts are returned
- [ ] Verify the optional `?threshold=critical` query parameter returns a filtered response without errors

## Dependencies
- Depends on: Task 1 — Add advisory severity count model and service method
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summaries in ingestion pipeline
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
