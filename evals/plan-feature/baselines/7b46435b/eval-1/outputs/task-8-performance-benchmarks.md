# Task 8 — Performance Benchmarks for advisory severity aggregation feature

## Repository
trustify-backend

## Target Branch
main

## Description
Validate cross-cutting performance benchmark criteria for the advisory severity aggregation feature (TC-9001). Verify that the advisory-summary endpoint meets the p95 < 200ms response time requirement for SBOMs with up to 500 advisories, that no memory leaks are detected during sustained usage, and that database query performance does not degrade with increased data volume. This task covers the "Performance Benchmarks" category from the testing readiness template.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Performance test: GET /api/v2/sbom/{id}/advisory-summary p95 response time < 200ms for an SBOM with 500 advisories
- [ ] Performance test: sustained load (100 requests/second for 5 minutes) shows no memory leak (RSS remains stable)
- [ ] Performance test: response time does not degrade when SBOM count increases from 100 to 10,000 SBOMs in the database
- [ ] Performance test: aggregation query execution plan uses indexes on sbom_advisory join table (no full table scans)
- [ ] Performance test: cached responses return in < 10ms (verify cache hit performance)

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute caching
- Depends on: Task 3 — Add cache invalidation for advisory-summary on advisory ingestion
- Depends on: Task 4 — Add threshold query parameter to advisory-summary endpoint (non-MVP)
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
