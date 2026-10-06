## Repository
trustify-backend

## Target Branch
main

## Description
Validate the advisory severity aggregation feature (TC-9001) against the Smoke Tests criteria from the testing readiness template. This cross-cutting testing task verifies that all new and modified API endpoints function correctly with valid inputs, maintain backward compatibility, and support the end-to-end workflow.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid SBOM ID and correct JSON response shape
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with filtered severity counts
- [ ] Existing `GET /api/v2/sbom/{id}` endpoint is unaffected by the new endpoint addition
- [ ] Existing `GET /api/v2/sbom/{id}/advisories` endpoint continues to work as before
- [ ] End-to-end workflow: ingest SBOM, ingest advisory, correlate, call advisory-summary, verify counts are correct

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and severity aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache
- Depends on: Task 3 — Add cache invalidation for advisory summaries in advisory ingestion pipeline
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
- Depends on: Task 5 — Add optional threshold query parameter for severity filtering
