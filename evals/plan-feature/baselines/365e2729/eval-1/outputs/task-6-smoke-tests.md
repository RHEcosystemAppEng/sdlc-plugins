## Repository
trustify-backend

## Target Branch
main

## Description
Run feature-level smoke tests for TC-9001 (advisory severity aggregation endpoint) per the "Smoke Tests" category of the repository's testing readiness template (`docs/testing-readiness.md`). Validate that the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint works with valid inputs, that existing SBOM and advisory endpoints remain backward compatible, and that the end-to-end workflow (ingest SBOM → ingest/correlate advisories → query summary → ingest new advisory → query refreshed summary) completes without errors.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` for an ingested SBOM with correlated advisories
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with only the critical count
- [ ] Existing endpoints `GET /api/v2/sbom`, `GET /api/v2/sbom/{id}`, `GET /api/v2/sbom/{id}/advisories`, `GET /api/v2/advisory`, and `GET /api/v2/advisory/{id}` return the same status codes and response shapes as before the feature
- [ ] End-to-end: ingest an SBOM, ingest advisories that correlate to it, call the summary endpoint and confirm counts match `GET /api/v2/sbom/{id}/advisories` counted by severity (unique advisories), ingest an additional advisory and confirm the summary updates without waiting for cache TTL
- [ ] Unknown SBOM ID returns 404 from the summary endpoint

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Invalidate advisory-summary cache on advisory ingestion
- Depends on: Task 4 — Add optional severity threshold filter to advisory-summary endpoint
