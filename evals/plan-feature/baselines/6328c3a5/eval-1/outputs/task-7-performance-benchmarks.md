## Repository
trustify-backend

## Target Branch
main

## Description
Perform performance benchmark testing for the advisory severity aggregation feature (TC-9001). Validate that API response times are within acceptable thresholds under load, that no memory leaks are detected during sustained usage, and that database query performance does not degrade with increased data volume.

This testing task covers the cross-cutting **Performance Benchmarks** category from the testing readiness template at `docs/testing-readiness.md`.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` responds within p95 < 200ms for SBOMs with up to 500 advisories (per the feature's non-functional requirements)
- [ ] Response time remains stable under concurrent requests (10+ simultaneous calls to the advisory-summary endpoint)
- [ ] Memory usage does not grow unbounded during repeated calls to the advisory-summary endpoint over a sustained period
- [ ] Database aggregation query time does not degrade when the `sbom_advisory` table grows (test with 1000+ advisory-SBOM relationship records)
- [ ] Cache hits return responses significantly faster than cache misses (verify caching provides measurable improvement)

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation endpoint
- Depends on: Task 2 — Add cache invalidation for advisory severity summaries
- Depends on: Task 3 — Add integration tests for advisory-summary endpoint
- Depends on: Task 4 — Add optional severity threshold filter
