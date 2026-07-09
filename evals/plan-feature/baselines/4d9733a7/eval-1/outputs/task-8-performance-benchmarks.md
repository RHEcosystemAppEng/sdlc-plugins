## Repository
trustify-backend

## Target Branch
main

## Description
Execute performance benchmarks for the advisory severity aggregation feature (TC-9001) to validate that the new endpoint meets the non-functional requirements: p95 response time under 200ms for SBOMs with up to 500 advisories, no memory leaks under sustained usage, and no database query degradation with increased data volume. This testing task covers the "Performance Benchmarks" category from the testing readiness template.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Benchmark `GET /api/v2/sbom/{id}/advisory-summary` response time with an SBOM linked to 500 advisories — verify p95 < 200ms
- [ ] Benchmark response time with an SBOM linked to 1000 advisories to verify performance scaling
- [ ] Monitor memory usage during 100 consecutive requests to detect leaks
- [ ] Verify that the aggregation query execution plan uses indexes effectively (no full table scans on the `sbom_advisory` join table)
- [ ] Verify cached response time is significantly faster than uncached (< 10ms for cached vs < 200ms for uncached)

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summaries
- Depends on: Task 4 — Add threshold query parameter support
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
