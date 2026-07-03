# Task 7 — Smoke Tests for advisory severity aggregation feature

## Repository
trustify-backend

## Target Branch
main

## Description
Validate cross-cutting smoke test criteria for the advisory severity aggregation feature (TC-9001). Verify that all new API endpoints return successful responses with valid inputs, that modified endpoints maintain backward compatibility, and that the end-to-end workflow completes without errors. This task covers the "Smoke Tests" category from the testing readiness template.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Smoke test: GET /api/v2/sbom/{id}/advisory-summary with a valid SBOM returns 200 OK with correct JSON shape
- [ ] Smoke test: GET /api/v2/sbom/{id}/advisory-summary with threshold parameter returns 200 OK with filtered response
- [ ] Smoke test: existing SBOM endpoints (GET /api/v2/sbom, GET /api/v2/sbom/{id}) continue to function correctly after changes
- [ ] Smoke test: existing advisory endpoints (GET /api/v2/advisory, GET /api/v2/advisory/{id}) continue to function correctly
- [ ] Smoke test: end-to-end flow — ingest SBOM, ingest advisories, call advisory-summary, verify counts

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute caching
- Depends on: Task 3 — Add cache invalidation for advisory-summary on advisory ingestion
- Depends on: Task 4 — Add threshold query parameter to advisory-summary endpoint (non-MVP)
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
