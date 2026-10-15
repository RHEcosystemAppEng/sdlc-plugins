## Repository
trustify-backend

## Target Branch
main

## Description
Perform smoke testing for the advisory severity aggregation feature (TC-9001). Validate that all new and modified API endpoints return successful responses with valid inputs, maintain backward compatibility on existing endpoints, and that the end-to-end workflow (SBOM ingestion, advisory correlation, severity summary retrieval) completes without errors.

This task validates the acceptance criteria from the testing readiness template's Smoke Tests category.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with a valid JSON response containing critical, high, medium, low, and total fields when called with a valid SBOM ID
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 404 when called with a non-existent SBOM ID
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with filtered counts
- [ ] Existing `GET /api/v2/sbom/{id}` endpoint continues to return the same response shape (backward compatibility)
- [ ] Existing `GET /api/v2/advisory` and `GET /api/v2/advisory/{id}` endpoints are unaffected
- [ ] End-to-end workflow: ingest an SBOM, ingest advisories that correlate to it, then call the advisory-summary endpoint and verify counts match the ingested data

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model, service, and endpoint
- Depends on: Task 2 — Add cache invalidation for advisory-summary on advisory ingestion
- Depends on: Task 3 — Add threshold query parameter for advisory-summary endpoint
