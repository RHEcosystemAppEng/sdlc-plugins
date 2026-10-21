## Repository
trustify-backend

## Target Branch
main

## Description
Execute cross-cutting performance benchmarks to validate that the advisory severity aggregation feature (TC-9001) meets non-functional requirements after all implementation tasks are complete. This testing task covers the Performance Benchmarks category from the testing readiness template, verifying that API response time is within acceptable thresholds under load, no memory leaks are detected during sustained usage, and database query performance does not degrade with increased data volume. The feature requires p95 response time under 200ms for SBOMs with up to 500 advisories.

Ref: TC-9001

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Performance benchmark: measure p95 response time for GET /api/v2/sbom/{id}/advisory-summary with an SBOM linked to 500 advisories; verify p95 < 200ms
- [ ] Performance benchmark: measure response time with cache warm (second call within 5 minutes) vs cache cold (first call); verify cache reduces latency
- [ ] Performance benchmark: sustained load test calling the advisory-summary endpoint repeatedly for 5 minutes; monitor memory usage for leaks
- [ ] Performance benchmark: measure query performance with increasing advisory counts (100, 250, 500 advisories) to verify no degradation

## Dependencies
- Depends on: Task 1 -- Add AdvisorySeveritySummary model and aggregation service method
- Depends on: Task 2 -- Add advisory-summary endpoint with caching
- Depends on: Task 3 -- Add cache invalidation for advisory summaries
- Depends on: Task 4 -- Add threshold query parameter filtering
