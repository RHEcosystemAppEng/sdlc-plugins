## Repository
trustify-backend

## Target Branch
main

## Description
Execute performance benchmarks for the advisory severity aggregation feature (TC-9001) to validate that the advisory-summary endpoint meets the p95 < 200ms latency requirement for SBOMs with up to 500 advisories, that no memory leaks occur during sustained usage, and that database query performance does not degrade with increased data volume. This cross-cutting testing task verifies feature-level readiness per the testing readiness template's Performance Benchmarks category.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Benchmark GET /api/v2/sbom/{id}/advisory-summary with an SBOM linked to 500 advisories; verify p95 response time < 200ms
- [ ] Benchmark GET /api/v2/sbom/{id}/advisory-summary with an SBOM linked to 10, 100, and 500 advisories; verify response time scales linearly (no exponential degradation)
- [ ] Run sustained load test (repeated requests over 5 minutes) and monitor for memory growth indicating leaks
- [ ] Verify that the advisory severity aggregation SQL query uses appropriate indexes on the sbom_advisory join table and does not perform a full table scan
- [ ] Benchmark with and without cache: verify cached responses return in < 5ms; verify uncached responses return in < 200ms for 500 advisories

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching and threshold filter
- Depends on: Task 3 — Add cache invalidation for advisory summaries on advisory ingestion
