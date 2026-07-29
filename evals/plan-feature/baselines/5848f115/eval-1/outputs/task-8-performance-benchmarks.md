## Repository
trustify-backend

## Target Branch
main

## Description
Execute performance benchmark tests for the advisory severity aggregation feature (TC-9001) to validate that the new endpoint meets the non-functional requirements: p95 response time under 200ms for SBOMs with up to 500 advisories, no memory leaks during sustained usage, and no database query performance degradation with increased data volume. This is a cross-cutting validation activity based on the testing readiness template at `docs/testing-readiness.md`.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Performance test: `GET /api/v2/sbom/{id}/advisory-summary` p95 response time < 200ms for an SBOM with 500 linked advisories
- [ ] Performance test: sustained load (e.g., 100 requests/second for 5 minutes) does not cause memory growth beyond baseline
- [ ] Performance test: response time remains < 200ms when the total advisory count in the database grows from 100 to 10,000
- [ ] Performance test: cache hit response time is significantly faster than cache miss (validating the 5-minute cache)
- [ ] Performance test: the advisory-summary endpoint under load does not degrade performance of existing endpoints (e.g., `GET /api/v2/sbom/{id}`)

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service layer
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation in advisory ingestion pipeline
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
- Depends on: Task 5 — Add optional threshold query parameter
