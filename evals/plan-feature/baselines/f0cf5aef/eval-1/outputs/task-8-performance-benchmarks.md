## Repository
trustify-backend

## Target Branch
main

## Description
Validate the advisory severity aggregation feature (TC-9001) against the Performance Benchmarks criteria from the testing readiness template. This cross-cutting testing task verifies that the new endpoint meets the non-functional performance requirements: p95 response time under 200ms for SBOMs with up to 500 advisories, no memory leaks, and stable database query performance under increasing data volume.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Benchmark `GET /api/v2/sbom/{id}/advisory-summary` with an SBOM linked to 500 advisories; verify p95 response time is under 200ms
- [ ] Benchmark the endpoint under concurrent load (e.g., 50 concurrent requests) to verify stable response times
- [ ] Profile memory usage during sustained advisory-summary requests to detect leaks
- [ ] Test with progressively larger advisory counts (100, 250, 500) to verify query performance does not degrade significantly
- [ ] Verify that the 5-minute cache provides expected performance improvement on repeated requests

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and severity aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache
- Depends on: Task 3 — Add cache invalidation for advisory summaries in advisory ingestion pipeline
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
- Depends on: Task 5 — Add optional threshold query parameter for severity filtering
