## Repository
trustify-backend

## Target Branch
main

## Description
Execute performance benchmarks to validate that the advisory severity aggregation feature (TC-9001) meets the non-functional performance requirements from the testing readiness template. This cross-cutting validation ensures that API response times are within acceptable thresholds under load, no memory leaks are detected, and database query performance does not degrade with increased data volume.

The feature specifies a p95 response time target of < 200ms for SBOMs with up to 500 advisories, and alerting if p95 exceeds 500ms.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Performance test: GET /api/v2/sbom/{id}/advisory-summary responds within p95 < 200ms for an SBOM with 500 advisories
- [ ] Performance test: sustained load (repeated requests over 5 minutes) does not increase memory usage beyond baseline
- [ ] Performance test: response time does not degrade when the number of advisories linked to an SBOM increases from 10 to 500
- [ ] Performance test: aggregation query execution plan does not show sequential scans on large tables

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory ingestion
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
