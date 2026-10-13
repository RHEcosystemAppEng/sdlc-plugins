## Repository
trustify-backend

## Target Branch
main

## Description
Execute performance benchmarks for the advisory severity summary feature to verify that API response times are within acceptable thresholds under load, no memory leaks are detected during sustained usage, and database query performance does not degrade with increased data volume.

## Acceptance Criteria
- [ ] API response time for GET /api/v2/sbom/{id}/advisory-summary is p95 < 200ms for SBOMs with up to 500 advisories
- [ ] No memory leaks detected during sustained usage of the advisory-summary endpoint
- [ ] Database query performance for severity aggregation does not degrade as advisory count increases from 100 to 500 to 1000

## Test Requirements
- [ ] Load test: advisory-summary endpoint under concurrent requests (50 concurrent users) maintains p95 < 200ms
- [ ] Sustained usage test: repeated advisory-summary calls over 10 minutes show stable memory usage (no growth trend)
- [ ] Data volume test: measure query time with 100, 500, and 1000 advisories linked to a single SBOM, verify sub-linear or linear scaling
- [ ] Cache effectiveness test: verify cache hit ratio exceeds 80% under realistic access patterns with 5-minute TTL

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service layer
- Depends on: Task 2 — Add advisory-summary endpoint with response caching
- Depends on: Task 3 — Invalidate advisory-summary cache on advisory ingestion
