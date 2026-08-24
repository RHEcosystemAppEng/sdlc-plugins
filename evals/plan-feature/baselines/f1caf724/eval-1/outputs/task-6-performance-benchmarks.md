## Repository
trustify-backend

## Target Branch
main

## Description
Perform performance benchmarking for the TC-9001 advisory severity aggregation feature. Validate that the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint meets the p95 < 200ms response time requirement for SBOMs with up to 500 advisories, that no memory leaks are detected during sustained usage, and that the underlying database query performance does not degrade with increased data volume. This testing task covers the Performance Benchmarks category from the project's testing readiness template.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Benchmark `GET /api/v2/sbom/{id}/advisory-summary` response time with an SBOM linked to 500 advisories and verify p95 < 200ms
- [ ] Benchmark the endpoint under concurrent load (multiple simultaneous requests) and verify response times remain within threshold
- [ ] Monitor memory usage during sustained repeated calls to the endpoint and verify no memory leak pattern
- [ ] Benchmark the aggregation query with progressively larger advisory counts (100, 250, 500) and verify query time scales acceptably
- [ ] Verify that cached responses return significantly faster than uncached responses (cache hit vs cache miss latency comparison)

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summary on advisory ingestion
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
