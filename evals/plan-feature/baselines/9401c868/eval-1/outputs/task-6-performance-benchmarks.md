## Repository
trustify-backend

## Target Branch
main

## Description
Perform cross-cutting performance benchmark testing for the advisory severity aggregation feature (TC-9001). Validate that the new advisory summary endpoint meets the p95 < 200ms response time requirement for SBOMs with up to 500 advisories, that no memory leaks are detected during sustained usage of the endpoint, and that the aggregation query does not degrade database performance with increased data volume.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Performance benchmark: `GET /api/v2/sbom/{id}/advisory-summary` responds within p95 < 200ms for an SBOM with 500 advisories
- [ ] Performance benchmark: endpoint response time under concurrent load (e.g., 50 concurrent requests) remains within acceptable thresholds
- [ ] Performance benchmark: memory usage remains stable after 1000 consecutive requests to the advisory summary endpoint
- [ ] Performance benchmark: aggregation query execution time does not degrade significantly when the advisory count increases from 100 to 500 to 1000
- [ ] Performance benchmark: cached responses return within p95 < 10ms (cache hit performance)

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
- Depends on: Task 2 — Add advisory severity summary endpoint with caching and threshold filter
- Depends on: Task 3 — Add cache invalidation for advisory summaries in the ingestor
