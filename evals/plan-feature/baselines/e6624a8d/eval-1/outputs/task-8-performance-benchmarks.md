## Repository
trustify-backend

## Target Branch
main

## Description
Execute cross-cutting performance benchmarks for the advisory severity aggregation feature (TC-9001). These benchmarks validate that the new advisory-summary endpoint meets the p95 < 200ms response time requirement for SBOMs with up to 500 advisories, that no memory leaks are detected during sustained usage of the endpoint, and that the aggregation query performance does not degrade with increased advisory data volume.

Test category: Performance Benchmarks (from testing readiness template).

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Performance benchmark: `GET /api/v2/sbom/{id}/advisory-summary` p95 response time < 200ms for SBOMs with up to 500 advisories
- [ ] Performance benchmark: sustained load test (repeated calls over 5 minutes) shows no memory growth in the server process
- [ ] Performance benchmark: response time remains stable as the number of advisories per SBOM increases from 10 to 100 to 500
- [ ] Performance benchmark: verify the 5-minute cache reduces database load under repeated identical requests

## Dependencies
- Depends on: Task 1 — Add advisory severity summary response model
- Depends on: Task 2 — Add advisory severity aggregation service method
- Depends on: Task 3 — Add advisory-summary REST endpoint with caching
- Depends on: Task 4 — Add cache invalidation for advisory ingestion
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
