## Repository
trustify-backend

## Target Branch
main

## Description
Run cross-cutting smoke tests for TC-9001 (advisory severity aggregation endpoint), following the "Smoke Tests" category of the repository's testing readiness template (`docs/testing-readiness.md`). The goal is to confirm that the new endpoint works end to end and that existing SBOM/advisory endpoints still behave as before.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` for an ingested SBOM with correlated advisories
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with only the critical count
- [ ] Existing `GET /api/v2/sbom`, `GET /api/v2/sbom/{id}`, `GET /api/v2/sbom/{id}/advisories`, `GET /api/v2/advisory`, and `GET /api/v2/advisory/{id}` responses are unchanged (backward compatibility)
- [ ] End-to-end: ingest SBOM → ingest correlated advisory → call advisory-summary → counts match the number of unique advisories reported by `GET /api/v2/sbom/{id}/advisories` per severity (UC-1)
- [ ] End-to-end: ingest an additional advisory → summary reflects it (cache invalidation)
- [ ] Unknown SBOM ID returns 404

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Invalidate cached advisory summaries on advisory ingestion
- Depends on: Task 4 — Add optional threshold query parameter to advisory-summary endpoint
