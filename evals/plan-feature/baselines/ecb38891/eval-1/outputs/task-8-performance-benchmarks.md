## Repository
trustify-backend

## Target Branch
main

## Description
Validate the performance benchmark criteria from the testing readiness template for the advisory severity aggregation feature (TC-9001). This cross-cutting testing task verifies that the new endpoint meets performance requirements: API response time within acceptable thresholds under load (p95 < 200ms for SBOMs with up to 500 advisories), no memory leaks during sustained usage, and database query performance does not degrade with increased data volume.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Benchmark `GET /api/v2/sbom/{id}/advisory-summary` response time with an SBOM linked to 500 advisories; verify p95 < 200ms
- [ ] Benchmark response time with SBOMs of varying advisory counts (10, 50, 100, 500) to confirm linear or sub-linear scaling
- [ ] Monitor memory usage during sustained repeated requests to the advisory summary endpoint; verify no memory leak
- [ ] Test database query plan for the severity aggregation query with 500+ advisory links to verify index usage and absence of full table scans
- [ ] Verify cached responses return in < 10ms (cache hit performance)

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service
- Depends on: Task 2 — Add advisory summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory severity summary
- Depends on: Task 4 — Add threshold query parameter for advisory summary
- Depends on: Task 5 — Add integration tests for advisory summary endpoint
