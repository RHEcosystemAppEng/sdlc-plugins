## Repository
trustify-backend

## Target Branch
main

## Description
Execute performance benchmarks for the advisory severity aggregation feature (TC-9001) to validate that the new endpoint meets the non-functional requirement of p95 < 200ms for SBOMs with up to 500 advisories, that no memory leaks are detected during sustained usage, and that the database query performance does not degrade with increased data volume. This task validates the "Performance Benchmarks" category from the testing readiness template.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Benchmark `GET /api/v2/sbom/{id}/advisory-summary` with an SBOM linked to 500 advisories; verify p95 response time < 200ms
- [ ] Benchmark the endpoint under sustained concurrent load (e.g., 50 concurrent requests over 60 seconds); monitor memory usage for leaks
- [ ] Benchmark the aggregation query with increasing data volume (100, 250, 500 advisories per SBOM); verify query time does not degrade disproportionately
- [ ] Verify cache effectiveness: measure response times for cached vs uncached requests; cached responses should be significantly faster

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and aggregation service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summaries during advisory ingestion
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
