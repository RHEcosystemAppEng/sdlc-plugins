## Repository
trustify-backend

## Target Branch
main

## Description
Execute performance benchmark tests for the advisory severity aggregation feature (TC-9001) to verify that the API response time meets the p95 < 200ms requirement for SBOMs with up to 500 advisories, that no memory leaks occur during sustained usage, and that database query performance does not degrade with increased data volume. This task validates the testing readiness criteria from the "Performance Benchmarks" category in the repository's testing readiness template.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Performance test: `GET /api/v2/sbom/{id}/advisory-summary` achieves p95 < 200ms for an SBOM with 500 linked advisories
- [ ] Performance test: sustained load (e.g., 100 requests/second for 60 seconds) does not cause memory growth beyond acceptable bounds
- [ ] Performance test: response time for an SBOM with 10 advisories vs 500 advisories shows linear or sub-linear scaling (no exponential degradation)
- [ ] Performance test: cache hit performance is significantly faster than cache miss performance (validating the 5-minute cache)
- [ ] Performance test: the aggregation query does not cause full table scans on the `sbom_advisory` join table (verify via EXPLAIN ANALYZE)

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
- Depends on: Task 3 — Add cache invalidation in advisory ingestion pipeline
- Depends on: Task 4 — Add optional threshold query parameter for severity filtering
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
