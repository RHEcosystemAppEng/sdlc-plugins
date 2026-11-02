## Repository
trustify-backend

## Target Branch
main

## Description
Execute cross-cutting performance benchmarks for the TC-9001 advisory severity aggregation feature. Validate that API response times are within acceptable thresholds under load, no memory leaks are detected during sustained usage, and database query performance does not degrade with increased data volume. The feature requires p95 response time < 200ms for SBOMs with up to 500 advisories.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Benchmark: `GET /api/v2/sbom/{id}/advisory-summary` p95 response time < 200ms with an SBOM linked to 500 advisories
- [ ] Benchmark: sustained load test (e.g., 100 requests/second for 60 seconds) shows no memory growth
- [ ] Benchmark: query execution time for the aggregation query remains stable as advisory count increases from 100 to 500 to 1000
- [ ] Benchmark: cached response time is significantly lower than uncached response time

## Dependencies
- Depends on: Task 1 — Advisory severity summary model
- Depends on: Task 2 — Advisory summary aggregation service
- Depends on: Task 3 — Advisory summary endpoint with caching
- Depends on: Task 4 — Cache invalidation on advisory ingestion
- Depends on: Task 5 — Threshold query parameter filter
- Depends on: Task 6 — Integration tests for advisory summary
