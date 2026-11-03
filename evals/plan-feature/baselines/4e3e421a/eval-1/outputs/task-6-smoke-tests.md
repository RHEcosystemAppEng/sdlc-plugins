## Repository
trustify-backend

## Target Branch
main

## Description
Run feature-level smoke tests for Feature TC-9001 (advisory severity aggregation endpoint), following the "Smoke Tests" category of the repository's testing readiness template (`docs/testing-readiness.md`). The goal is to confirm that the new endpoint works end to end with valid inputs, that existing SBOM and advisory endpoints stay backward compatible, and that the full UC-1 workflow completes without errors: ingest SBOM, correlate advisories, fetch the summary, ingest a new advisory, and fetch the refreshed summary.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` for an ingested SBOM with correlated advisories
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for a non-existent SBOM ID
- [ ] If Task 4 shipped: `?threshold=critical` returns 200 with only the critical count
- [ ] Backward compatibility: `GET /api/v2/sbom`, `GET /api/v2/sbom/{id}`, `GET /api/v2/sbom/{id}/advisories`, `GET /api/v2/advisory`, and `GET /api/v2/advisory/{id}` return the same status codes and response shapes as before the feature
- [ ] End-to-end (UC-1): ingest an SBOM, run advisory correlation, call the summary endpoint, and verify that the counts match the correlated advisories (deduplicated)
- [ ] End-to-end (cache invalidation): after the first summary call, ingest a new advisory linked to the SBOM and confirm that the next summary call reflects it without waiting 5 minutes
- [ ] The summary counts match a client-side count over all pages of `GET /api/v2/sbom/{id}/advisories`, deduplicated by advisory ID, which confirms parity with the workflow being replaced

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service aggregation
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Invalidate cached advisory summaries on advisory ingestion
- Depends on: Task 4 — Add optional threshold query parameter
