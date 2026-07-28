# Task 6 — Smoke tests for advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Perform smoke testing for the advisory severity aggregation feature (TC-9001). Validate that the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns successful responses with valid inputs, that existing SBOM and advisory endpoints maintain backward compatibility, and that the end-to-end workflow (SBOM ingestion, advisory correlation, summary retrieval) completes without errors.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid JSON for a known SBOM with advisories
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}` endpoint continues to work after the changes
- [ ] Smoke test: existing `GET /api/v2/advisory` endpoint continues to work after the changes
- [ ] Smoke test: ingest an SBOM, correlate advisories, call `advisory-summary` — full workflow completes without errors
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with valid JSON

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory severity summaries in ingestion pipeline
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
