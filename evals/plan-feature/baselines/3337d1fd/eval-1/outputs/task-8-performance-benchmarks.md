## Repository
trustify-backend

## Target Branch
main

## Description
Execute performance benchmarks to validate that the advisory severity aggregation endpoint meets the non-functional requirements. Verify that API response time is within acceptable thresholds under load (p95 < 200ms for SBOMs with up to 500 advisories), that no memory leaks are detected during sustained usage, and that database query performance does not degrade with increased data volume.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] p95 response time for `GET /api/v2/sbom/{id}/advisory-summary` is under 200ms with up to 500 advisories
- [ ] No memory leaks detected during sustained usage of the advisory-summary endpoint
- [ ] Database query performance does not degrade with increased data volume
- [ ] Cache hit responses are significantly faster than cache miss responses

## Test Requirements
- [ ] Performance benchmark: measure p95 response time for advisory-summary with 100, 250, and 500 advisories
- [ ] Performance benchmark: sustained load test over 10 minutes to detect memory leaks
- [ ] Performance benchmark: measure query execution time with increasing SBOM-advisory relationship counts
- [ ] Performance benchmark: verify cache effectiveness by comparing cached vs uncached response times

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model
- Depends on: Task 2 — Implement advisory severity aggregation service
- Depends on: Task 3 — Add advisory-summary endpoint with caching
- Depends on: Task 4 — Add cache invalidation on advisory ingestion
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint