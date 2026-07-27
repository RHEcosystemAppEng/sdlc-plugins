# Task 8 — Performance Benchmarks for advisory severity aggregation feature

## Repository
trustify-backend

## Target Branch
main

## Description
Execute cross-cutting performance benchmarks to validate the advisory severity aggregation feature meets its non-functional requirements. This testing task covers the Performance Benchmarks category from the testing readiness template, verifying that API response time is within acceptable thresholds under load, no memory leaks are detected during sustained usage, and database query performance does not degrade with increased data volume.

Reference: Feature TC-9001 — Add advisory severity aggregation endpoint. Non-functional requirement: p95 < 200ms for SBOMs with up to 500 advisories.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Performance benchmark: `GET /api/v2/sbom/{id}/advisory-summary` responds within p95 < 200ms for an SBOM with 500 linked advisories
- [ ] Performance benchmark: response time does not degrade when SBOM has 100, 250, and 500 advisories (linear or sub-linear scaling)
- [ ] Performance benchmark: sustained repeated requests to the endpoint do not cause memory growth (validates cache does not leak)
- [ ] Performance benchmark: database query execution plan uses indexes on the `sbom_advisory` join table and does not perform full table scans
- [ ] Performance benchmark: endpoint under concurrent load (10+ simultaneous requests) maintains p95 < 200ms

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and severity aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Add threshold query parameter to advisory-summary endpoint
- Depends on: Task 4 — Add cache invalidation for advisory-summary on advisory ingestion
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
