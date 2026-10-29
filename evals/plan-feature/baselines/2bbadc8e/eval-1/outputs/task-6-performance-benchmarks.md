## Repository
trustify-backend

## Target Branch
main

## Description
Execute performance benchmark tests for the advisory severity aggregation feature (TC-9001). Verify that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint meets the p95 < 200ms response time requirement for SBOMs with up to 500 advisories, that no memory leaks are detected during sustained usage, and that database query performance does not degrade with increased data volume.

These tests validate the readiness criteria from the testing readiness template's Performance Benchmarks category. The feature's non-functional requirements specify p95 < 200ms for SBOMs with up to 500 advisories.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Performance test: `GET /api/v2/sbom/{id}/advisory-summary` returns within 200ms at p95 for an SBOM with 500 correlated advisories
- [ ] Performance test: sustained repeated advisory-summary queries (1000+ requests) do not cause memory growth in the application process
- [ ] Performance test: advisory-summary query response time remains stable as the number of advisories per SBOM increases from 10 to 100 to 500
- [ ] Performance test: cache hit responses (within the 5-minute TTL) are significantly faster than cache miss responses

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory severity summaries
