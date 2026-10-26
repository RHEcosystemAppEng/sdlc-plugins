## Repository
trustify-backend

## Target Branch
main

## Description
Execute performance benchmarks for the advisory severity aggregation feature (TC-9001) to validate that the new endpoint meets response time requirements, does not introduce memory leaks, and maintains acceptable database query performance under load. This testing task covers the Performance Benchmarks category from the testing readiness template.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary` responds within p95 < 200ms for SBOMs with up to 500 linked advisories
- [ ] Verify response time remains under p95 < 200ms when serving from cache (within 5-minute TTL window)
- [ ] Verify response time for cache-miss requests (first request after cache expiration or invalidation) is within acceptable bounds
- [ ] Verify no memory growth over 1000 repeated requests to the advisory summary endpoint
- [ ] Verify the severity aggregation database query does not degrade as the number of advisories per SBOM increases from 10 to 100 to 500
- [ ] Verify concurrent requests (e.g., 50 simultaneous callers) do not cause connection pool exhaustion or elevated error rates

## Dependencies
- Depends on: Task 1 — Add advisory severity summary response model
- Depends on: Task 2 — Add SBOM advisory severity aggregation service method
- Depends on: Task 3 — Add advisory summary REST endpoint with caching
- Depends on: Task 4 — Add cache invalidation on advisory ingestion
- Depends on: Task 5 — Add integration tests for advisory summary endpoint
