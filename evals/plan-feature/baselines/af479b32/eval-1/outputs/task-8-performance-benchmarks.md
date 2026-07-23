## Repository
trustify-backend

## Target Branch
main

## Description
Perform performance benchmarking for the advisory severity aggregation feature (TC-9001). Validate that the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint meets the non-functional requirement of p95 response time < 200ms for SBOMs with up to 500 advisories. Check for memory leaks during sustained usage and verify that the aggregation query performance does not degrade with increased advisory data volume.

This testing task covers the "Performance Benchmarks" category from the testing readiness template at `docs/testing-readiness.md`.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Performance test: `GET /api/v2/sbom/{id}/advisory-summary` p95 response time is < 200ms for an SBOM with 500 correlated advisories
- [ ] Performance test: sustained rapid requests to the advisory-summary endpoint do not cause memory growth (verify with process memory monitoring)
- [ ] Performance test: advisory-summary query time for SBOMs with 100, 250, and 500 advisories shows acceptable scaling behavior (sub-linear growth preferred)
- [ ] Performance test: verify that the 5-minute cache reduces p95 response time on repeated requests to the same SBOM
- [ ] Performance test: advisory ingestion with cache invalidation does not introduce significant latency overhead compared to ingestion without the feature

## Dependencies
- Depends on: Task 1 — Add severity aggregation model and service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summaries
- Depends on: Task 4 — Add threshold query parameter support
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
