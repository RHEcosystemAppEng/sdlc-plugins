## Repository
trustify-backend

## Target Branch
main

## Description
Execute cross-cutting performance benchmarks to validate that the advisory severity aggregation feature (TC-9001) meets the non-functional requirements defined in the feature specification. This testing task covers the Performance Benchmarks category from the testing readiness template, verifying that the new endpoint meets the p95 < 200ms response time target for SBOMs with up to 500 advisories, that no memory leaks are detected during sustained usage, and that database query performance does not degrade with increased data volume.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Performance benchmark: `GET /api/v2/sbom/{id}/advisory-summary` p95 response time < 200ms with SBOM containing 500 advisories
- [ ] Performance benchmark: sustained load test (1000 requests over 60 seconds) shows no memory leak (RSS stays stable)
- [ ] Performance benchmark: response time for SBOMs with 10, 100, and 500 advisories shows linear or sub-linear scaling (no N+1 query degradation)
- [ ] Performance benchmark: cached responses return within < 10ms (verifying cache effectiveness)

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and service method
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
- Depends on: Task 3 — Add cache invalidation in advisory ingestion pipeline
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
- Depends on: Task 5 — Add optional threshold query parameter support
