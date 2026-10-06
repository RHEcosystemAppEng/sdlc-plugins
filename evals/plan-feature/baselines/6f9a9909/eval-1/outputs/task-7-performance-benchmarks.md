## Repository
trustify-backend

## Target Branch
main

## Description
Execute performance benchmarks for the advisory severity aggregation feature (TC-9001) to verify that the new endpoint meets the non-functional performance requirements. This is a cross-cutting validation activity derived from the testing readiness template's Performance Benchmarks category.

The performance benchmarks should verify:
- API response time for `GET /api/v2/sbom/{id}/advisory-summary` is within the p95 < 200ms threshold for SBOMs with up to 500 advisories
- No memory leaks are detected during sustained usage of the advisory-summary endpoint
- Database query performance for the severity aggregation does not degrade with increased data volume (test with increasing numbers of advisories per SBOM)

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Performance benchmark: `GET /api/v2/sbom/{id}/advisory-summary` p95 response time < 200ms with 500 advisories linked to SBOM
- [ ] Performance benchmark: memory usage remains stable during repeated advisory-summary requests over a sustained period
- [ ] Performance benchmark: advisory-summary query time does not degrade significantly when scaling from 10 to 100 to 500 advisories per SBOM
- [ ] Performance benchmark: cached responses return within p95 < 10ms (cache-hit scenario)

## Dependencies
- Depends on: Task 1 — Create AdvisorySeveritySummary model and aggregation service
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation on advisory ingestion
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
