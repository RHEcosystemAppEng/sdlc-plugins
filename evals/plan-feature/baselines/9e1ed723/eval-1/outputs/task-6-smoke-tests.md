# Task 6 — Smoke Tests for advisory severity aggregation endpoint

**Summary:** TC-9001: Smoke Tests — advisory severity aggregation endpoint
**Issue type:** Task
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9001)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9001)

---

## Repository
trustify-backend

## Target Branch
main

## Description
Run the feature-level smoke tests for TC-9001 (Add advisory severity aggregation endpoint), as defined in the "Smoke Tests" category of the repository's testing readiness template (`docs/testing-readiness.md`). This checks that the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint (including the optional `threshold` parameter) responds correctly with valid inputs. It also checks that existing SBOM and advisory endpoints still behave as before, and that the full flow (ingest SBOM → ingest and correlate advisories → query summary → ingest another advisory → see refreshed summary) completes without errors.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` for an ingested SBOM with correlated advisories returns 200 with `critical`, `high`, `medium`, `low`, `total` and the correct counts
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with only the critical count
- [ ] `GET /api/v2/sbom/{unknown-id}/advisory-summary` returns 404
- [ ] Backward compatibility: `GET /api/v2/sbom`, `GET /api/v2/sbom/{id}`, `GET /api/v2/sbom/{id}/advisories`, `GET /api/v2/advisory`, and `GET /api/v2/advisory/{id}` return the same status codes and response shapes as before the feature
- [ ] End-to-end: ingest an SBOM, ingest advisories that correlate to it, query the summary, ingest an additional correlating advisory, query again, and confirm the counts update without waiting for the 5-minute TTL
- [ ] End-to-end: the dashboard flow (UC-1) can get severity counts with a single call instead of paging through `/advisories`

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and SbomService aggregation query
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 404 handling and 5-minute caching
- Depends on: Task 3 — Invalidate cached SBOM advisory summaries from the ingestion pipeline
- Depends on: Task 4 — Add optional ?threshold= severity filter to GET /api/v2/sbom/{id}/advisory-summary
