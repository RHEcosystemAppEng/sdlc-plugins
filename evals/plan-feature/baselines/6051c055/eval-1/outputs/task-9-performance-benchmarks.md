## Repository
trustify-backend

## Target Branch
main

## Description
Execute performance benchmarks to validate that the advisory severity aggregation endpoint meets latency and resource requirements. Verify that the endpoint responds within the p95 < 200ms threshold for SBOMs with up to 500 advisories, that no memory leaks occur under sustained load, and that existing database query performance does not degrade after the feature is deployed.

## Acceptance Criteria
- [ ] API response time within thresholds under load — p95 < 200ms for SBOMs with up to 500 advisories
- [ ] No memory leaks under sustained load against the advisory-summary endpoint
- [ ] DB query performance does not degrade — existing advisory and SBOM queries maintain pre-feature response times

## Test Requirements
- [ ] Performance test: GET /api/v2/sbom/{id}/advisory-summary responds within p95 < 200ms with 500 linked advisories
- [ ] Performance test: sustained load against the endpoint shows stable memory usage (no leaks)
- [ ] Performance test: existing SBOM and advisory endpoint response times are not regressed

## Dependencies
- Depends on: Task 1 — Advisory severity summary model
- Depends on: Task 2 — Advisory summary service
- Depends on: Task 3 — Advisory summary endpoint
- Depends on: Task 4 — Cache invalidation
- Depends on: Task 5 — Integration tests
- Depends on: Task 6 — Threshold query parameter
