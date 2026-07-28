# Task 7 — Performance benchmarks for advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Perform performance benchmark testing for the advisory severity aggregation feature (TC-9001). Validate that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint meets the p95 < 200ms response time requirement for SBOMs with up to 500 advisories, that no memory leaks are detected during sustained usage, and that the database query performance does not degrade with increased data volume.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Performance test: `GET /api/v2/sbom/{id}/advisory-summary` p95 response time < 200ms for an SBOM with 500 linked advisories
- [ ] Performance test: response time for the endpoint under concurrent load (e.g., 50 concurrent requests) remains under the 200ms p95 threshold
- [ ] Performance test: memory usage remains stable during 1000+ sequential requests to the advisory-summary endpoint
- [ ] Performance test: aggregation query performance is tested with SBOMs having 10, 100, and 500 advisories to verify no degradation
- [ ] Performance test: cached responses return within < 10ms (verifying cache effectiveness)

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory severity summaries in ingestion pipeline
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
