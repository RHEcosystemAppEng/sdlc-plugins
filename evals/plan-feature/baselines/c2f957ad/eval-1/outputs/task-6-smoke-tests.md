## Repository
trustify-backend

## Target Branch
main

## Description
Run the **Smoke Tests** category from the repository's testing readiness template (`docs/testing-readiness.md`) against the advisory severity aggregation feature (TC-9001). Confirm that the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint works with valid inputs, that existing SBOM and advisory endpoints remain backward compatible, and that the end-to-end flow (SBOM ingestion → advisory correlation → summary retrieval → cache invalidation) completes without errors.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` for an ingested SBOM with correlated advisories
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with the filtered response
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for an unknown SBOM ID
- [ ] Existing endpoints `GET /api/v2/sbom`, `GET /api/v2/sbom/{id}`, `GET /api/v2/sbom/{id}/advisories`, `GET /api/v2/advisory`, and `GET /api/v2/advisory/{id}` return unchanged responses (backward compatibility)
- [ ] End-to-end: ingest an SBOM, ingest correlated advisories, fetch the summary, ingest an additional advisory, and fetch again. Counts update with no errors in the server logs.
- [ ] Summary counts match a manual count of unique advisories from `GET /api/v2/sbom/{id}/advisories` for the same SBOM

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service aggregation
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Invalidate cached advisory summaries on advisory/SBOM ingestion
- Depends on: Task 4 — Support ?threshold query parameter on advisory-summary endpoint (non-MVP)
