## Repository
trustify-backend

## Target Branch
main

## Description
Run feature-level smoke tests for TC-9001 ("Add advisory severity aggregation endpoint"), following the **Smoke Tests** category of the repository's testing readiness template (`docs/testing-readiness.md`). The goal is to confirm that the new advisory severity summary endpoint responds correctly with valid inputs, that existing SBOM and advisory endpoints stay backward compatible, and that the end-to-end workflow (ingest SBOM → ingest and correlate advisories → request summary → ingest another advisory → request summary again) completes without errors.

Readiness template acceptance criteria covered by this task:
- All new API endpoints return successful responses with valid inputs
- All modified API endpoints maintain backward compatibility
- End-to-end workflow completes without errors

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` for an ingested SBOM with correlated advisories returns 200 with `critical`, `high`, `medium`, `low`, `total`, and the counts match the deduplicated advisories linked to the SBOM
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with only the critical count and `total` (if Task 3 has shipped)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` for an unknown SBOM ID returns 404, consistent with `GET /api/v2/sbom/{id}`
- [ ] Backward compatibility: `GET /api/v2/sbom`, `GET /api/v2/sbom/{id}`, `GET /api/v2/advisory`, `GET /api/v2/advisory/{id}`, and the existing SBOM advisory listing endpoint return the same status codes and response shapes as before the feature
- [ ] End-to-end: ingest an SBOM, ingest advisories that correlate to it, request the summary, ingest an additional advisory correlated to the same SBOM, and request the summary again. Every step succeeds, and the second summary reflects the new advisory without waiting for the 5-minute cache TTL.
- [ ] End-to-end: the summary counts match a client-side count of the paginated advisory listing for the same SBOM (deduplicated by advisory ID)

## Dependencies
- Depends on: Task 1 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
- Depends on: Task 2 — Cache advisory summary for 5 minutes with ingestion-driven invalidation
- Depends on: Task 3 — Add optional threshold filter to advisory summary endpoint
