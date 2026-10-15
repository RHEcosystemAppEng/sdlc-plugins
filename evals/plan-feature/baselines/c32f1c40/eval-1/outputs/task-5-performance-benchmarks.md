## Repository
trustify-backend

## Target Branch
main

## Description
Perform performance benchmark testing for the advisory severity aggregation feature (TC-9001). Validate that the advisory-summary endpoint meets the p95 < 200ms response time requirement for SBOMs with up to 500 advisories, that no memory leaks are detected during sustained usage, and that database query performance does not degrade with increased data volume.

This task validates the acceptance criteria from the testing readiness template's Performance Benchmarks category.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Benchmark `GET /api/v2/sbom/{id}/advisory-summary` with an SBOM linked to 500 advisories; verify p95 response time < 200ms
- [ ] Benchmark the endpoint under concurrent load (e.g., 50 concurrent requests) to verify response times remain within acceptable thresholds
- [ ] Run sustained load test (e.g., 1000 requests over 5 minutes) and monitor memory usage for leaks
- [ ] Test with increasing data volumes (100, 250, 500 advisories per SBOM) to verify query performance scales linearly or better
- [ ] Verify that the 5-minute cache improves response times on repeated requests (cache hit vs cache miss comparison)
- [ ] Benchmark with and without the `?threshold` query parameter to verify filtering does not add significant overhead

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model, service, and endpoint
- Depends on: Task 2 — Add cache invalidation for advisory-summary on advisory ingestion
- Depends on: Task 3 — Add threshold query parameter for advisory-summary endpoint
