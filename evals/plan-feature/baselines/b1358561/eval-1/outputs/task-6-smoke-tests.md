Summary: Smoke tests for advisory severity aggregation
Epic: TC-9001: Documentation and feature validation
Labels: ai-generated-jira | Priority: Major | Fix Version: RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Cross-cutting **Smoke Tests** validation for Feature TC-9001 (Add advisory severity
aggregation endpoint), derived from the "Smoke Tests" category of the repository's testing
readiness template (`docs/testing-readiness.md`). Validate that the new
`GET /api/v2/sbom/{id}/advisory-summary` endpoint works with valid inputs, that existing
SBOM/advisory endpoints remain backward compatible, and that the end-to-end workflow
(ingest SBOM → ingest/correlate advisories → query summary) completes without errors.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `critical`, `high`, `medium`, `low`, `total` for an ingested SBOM with correlated advisories
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with only the critical count populated
- [ ] Existing endpoints `GET /api/v2/sbom`, `GET /api/v2/sbom/{id}`, `GET /api/v2/sbom/{id}/advisories`, `GET /api/v2/advisory`, `GET /api/v2/advisory/{id}` return the same status codes and response shapes as before the feature
- [ ] End-to-end: ingest an SBOM, ingest an advisory that correlates to it, call the summary endpoint and confirm counts match the advisories listed by `GET /api/v2/sbom/{id}/advisories` (deduplicated)
- [ ] End-to-end: ingest an additional advisory and confirm the summary updates without waiting for cache TTL
- [ ] Unknown SBOM ID returns 404

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute caching
- Depends on: Task 3 — Invalidate cached advisory summaries on advisory and SBOM ingestion
- Depends on: Task 4 — Support optional ?threshold query parameter on advisory-summary
