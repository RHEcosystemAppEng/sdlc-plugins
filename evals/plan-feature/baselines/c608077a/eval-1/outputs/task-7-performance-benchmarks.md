## Repository
trustify-backend

## Target Branch
main

## Description
Run performance benchmarks for TC-9001 (advisory severity aggregation endpoint), following the "Performance Benchmarks" category of the repository's testing readiness template (`docs/testing-readiness.md`). The goal is to validate the feature's non-functional target of p95 < 200ms for SBOMs with up to 500 advisories.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Load test `GET /api/v2/sbom/{id}/advisory-summary` against an SBOM with 500 linked advisories: p95 < 200ms, measured both cold (cache miss) and warm (cache hit)
- [ ] Sustained load (e.g., 30 minutes of mixed SBOM IDs) shows stable process memory, with the cache bounded and not growing without limit
- [ ] Measure aggregation query time at 50, 500, and 5,000 advisories per SBOM and confirm it scales acceptably; inspect `EXPLAIN ANALYZE` to confirm index use on the `sbom_advisory` join
- [ ] Measure the impact on advisory ingestion throughput with cache invalidation enabled

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Invalidate cached advisory summaries on advisory ingestion
- Depends on: Task 4 — Add optional threshold query parameter to advisory-summary endpoint
