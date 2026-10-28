## Repository
trustify-backend

## Target Branch
main

## Description
Perform smoke testing for the advisory severity aggregation feature (TC-9001). Validate that all new and modified API endpoints return successful responses with valid inputs, that all modified API endpoints maintain backward compatibility, and that the end-to-end workflow completes without errors.

This testing task covers the cross-cutting **Smoke Tests** category from the testing readiness template at `docs/testing-readiness.md`.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid severity counts for a known SBOM with linked advisories
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with filtered severity counts
- [ ] Existing `GET /api/v2/sbom/{id}` endpoint continues to work unchanged (backward compatibility)
- [ ] Existing `GET /api/v2/advisory` and `GET /api/v2/advisory/{id}` endpoints continue to work unchanged (backward compatibility)
- [ ] Full end-to-end workflow: ingest SBOM, ingest advisories, correlate advisories to SBOM, then call `GET /api/v2/sbom/{id}/advisory-summary` and verify severity counts match the ingested data

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation endpoint
- Depends on: Task 2 — Add cache invalidation for advisory severity summaries
- Depends on: Task 3 — Add integration tests for advisory-summary endpoint
- Depends on: Task 4 — Add optional severity threshold filter
