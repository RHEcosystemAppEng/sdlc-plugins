## Repository
trustify-backend

## Target Branch
main

## Description
Execute cross-cutting performance benchmark tests for Feature TC-9001 (advisory severity aggregation endpoint) to validate that the feature meets non-functional performance requirements. This testing task covers the Performance Benchmarks category from the testing readiness template, verifying API response times, memory stability, and database query performance under load.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary` achieves p95 < 200ms for SBOMs with up to 500 advisories (per non-functional requirements)
- [ ] Verify no memory growth during sustained repeated calls to the advisory summary endpoint
- [ ] Verify aggregation query performance with increasing numbers of advisories linked to a single SBOM (100, 250, 500 advisories)
- [ ] Verify cache effectiveness: first call may be slower, subsequent cached calls should be significantly faster
- [ ] Verify cache invalidation does not introduce performance regression in the advisory ingestion pipeline

## Dependencies
- Depends on: Task 1 — Advisory severity summary model
- Depends on: Task 2 — Advisory summary service
- Depends on: Task 3 — Advisory summary endpoint
- Depends on: Task 4 — Cache invalidation
- Depends on: Task 5 — Integration tests
- Depends on: Task 6 — Threshold query param
