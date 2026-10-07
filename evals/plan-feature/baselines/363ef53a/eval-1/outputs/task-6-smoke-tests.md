## Repository
trustify-backend

## Target Branch
main

## Description
Execute smoke tests for the advisory severity aggregation feature (TC-9001) to validate that all new and modified API endpoints return successful responses with valid inputs, maintain backward compatibility on modified endpoints, and that the end-to-end workflow (ingestion, aggregation, cache invalidation) completes without errors. This task validates the "Smoke Tests" category from the testing readiness template.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid severity counts for an existing SBOM with linked advisories
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with filtered counts
- [ ] Verify existing `GET /api/v2/sbom/{id}` endpoint continues to work unchanged (backward compatibility)
- [ ] Verify existing `GET /api/v2/advisory` endpoint continues to work unchanged (backward compatibility)
- [ ] Verify end-to-end: ingest SBOM, ingest advisories, correlate, then call advisory-summary and confirm correct counts

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and aggregation service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summaries during advisory ingestion
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
