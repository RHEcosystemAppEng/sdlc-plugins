## Repository
trustify-backend

## Target Branch
main

## Description
Execute smoke tests for the advisory severity summary feature to verify that all new and modified API endpoints return successful responses with valid inputs, maintain backward compatibility, and that the end-to-end workflow completes without errors.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors: ingest SBOM, correlate advisories, call advisory-summary endpoint, verify correct severity counts

## Test Requirements
- [ ] GET /api/v2/sbom/{id}/advisory-summary returns 200 with valid SBOM ID and correct JSON structure
- [ ] GET /api/v2/sbom/{id}/advisory-summary returns 404 with non-existent SBOM ID
- [ ] GET /api/v2/sbom/{id}/advisory-summary?threshold=critical returns filtered response
- [ ] Existing GET /api/v2/sbom/{id} endpoint continues to function correctly (backward compatibility)
- [ ] Existing GET /api/v2/sbom/{id}/advisories endpoint continues to function correctly (backward compatibility)
- [ ] End-to-end: ingest SBOM, ingest advisory, verify advisory-summary reflects the linked advisory counts

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service layer
- Depends on: Task 2 — Add advisory-summary endpoint with response caching
- Depends on: Task 3 — Invalidate advisory-summary cache on advisory ingestion
