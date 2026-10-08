## Repository
trustify-backend

## Target Branch
main

## Description
Perform cross-cutting smoke testing for the advisory severity aggregation feature (TC-9001). Validate that all new API endpoints return successful responses with valid inputs, that all modified API endpoints maintain backward compatibility, and that the end-to-end workflow (SBOM ingestion, advisory correlation, severity summary retrieval) completes without errors.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid severity count JSON for an existing SBOM with advisories
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with filtered severity counts
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}` endpoint continues to return correct responses (backward compatibility)
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}/advisories` endpoint continues to return correct responses (backward compatibility)
- [ ] Smoke test: end-to-end workflow — ingest SBOM, ingest advisory, verify advisory-summary endpoint returns correct counts

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
- Depends on: Task 2 — Add advisory severity summary endpoint with caching and threshold filter
- Depends on: Task 3 — Add cache invalidation for advisory summaries in the ingestor
