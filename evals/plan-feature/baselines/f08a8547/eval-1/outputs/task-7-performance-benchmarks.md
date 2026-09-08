## Repository
trustify-backend

## Target Branch
main

## Description
Execute performance benchmark tests for the advisory severity aggregation feature (TC-9001) to verify that the new endpoint meets latency requirements, does not introduce memory leaks, and maintains database query performance at scale. This task validates the cross-cutting performance benchmark criteria from the testing readiness template.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Benchmark `GET /api/v2/sbom/{id}/advisory-summary` response time with SBOMs having up to 500 advisories; verify p95 < 200ms as specified in the feature's non-functional requirements
- [ ] Load test the endpoint with concurrent requests to verify response times remain stable under load
- [ ] Run sustained usage tests (repeated requests over time) and monitor memory usage for leaks in the aggregation query and caching layer
- [ ] Test the aggregation query performance with increasing advisory counts (100, 250, 500 advisories per SBOM) to verify that database query time does not degrade disproportionately
- [ ] Verify that the 5-minute cache reduces database load on repeated requests for the same SBOM

## Dependencies
- Depends on: Task 1 — Add advisory severity count model and service method
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summaries in ingestion pipeline
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
