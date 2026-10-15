## Repository
trustify-backend

## Target Branch
main

## Description
Execute performance benchmarks for the advisory severity aggregation feature (TC-9001) to validate that API response times are within acceptable thresholds under load, no memory leaks are detected during sustained usage, and database query performance does not degrade with increased data volume. This testing task covers the Performance Benchmarks category from the testing readiness template. The feature's non-functional requirement specifies p95 < 200ms for SBOMs with up to 500 advisories.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Benchmark `GET /api/v2/sbom/{id}/advisory-summary` response time with an SBOM linked to 500 advisories; verify p95 < 200ms
- [ ] Benchmark response time with an SBOM linked to 100 advisories under concurrent load (e.g., 50 concurrent requests)
- [ ] Verify no memory growth over 1000 repeated requests to the advisory-summary endpoint
- [ ] Benchmark the aggregation query performance with increasing advisory counts (100, 250, 500) to verify no query plan degradation
- [ ] Verify cached responses (within 5-minute TTL) are served in < 10ms

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching and threshold filter
- Depends on: Task 3 — Add cache invalidation in advisory ingestion pipeline
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
