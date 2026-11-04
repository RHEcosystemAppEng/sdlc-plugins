**Summary**: Smoke tests for advisory severity aggregation

## Repository
trustify-backend

## Target Branch
main

## Description
Cross-cutting **Smoke Tests** validation for Feature TC-9001 (advisory severity aggregation endpoint), derived from the repository's testing readiness template (`docs/testing-readiness.md`, category "Smoke Tests"). Confirm the new endpoint responds successfully with valid inputs, that existing SBOM/advisory endpoints remain backward compatible, and that the end-to-end flow (ingest SBOM → ingest/correlate advisories → query summary) completes without errors.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` for an ingested SBOM with correlated advisories
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with only the critical count
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for an unknown SBOM ID
- [ ] Existing endpoints `GET /api/v2/sbom`, `GET /api/v2/sbom/{id}`, `GET /api/v2/sbom/{id}/advisories`, `GET /api/v2/advisory`, `GET /api/v2/advisory/{id}` return unchanged responses (backward compatibility)
- [ ] Summary counts equal the number of unique advisories per severity obtained by paging `GET /api/v2/sbom/{id}/advisories` (parity with the current client-side counting)
- [ ] End-to-end: ingest an SBOM, ingest advisories that correlate to it, query the summary, ingest an additional advisory, and confirm the summary reflects it within the cache-invalidation path without errors

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and SBOM aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache
- Depends on: Task 3 — Invalidate cached advisory summaries on advisory ingestion
- Depends on: Task 4 — Support optional threshold query parameter on advisory-summary (non-MVP)
