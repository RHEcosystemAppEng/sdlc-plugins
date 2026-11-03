## Repository
trustify-backend

## Target Branch
main

## Description
Run performance benchmarks for Feature TC-9001 (advisory severity aggregation endpoint), following the "Performance Benchmarks" category of the repository's testing readiness template (`docs/testing-readiness.md`). The feature's non-functional requirements set a p95 response time below 200ms for SBOMs with up to 500 advisories. The goals are to cut summary load time from about 2s with the multi-page fetch to under 200ms, and to raise an operational alert if p95 exceeds 500ms. The benchmarks must measure both cold-cache and warm-cache behavior, so that the cache cannot mask a slow aggregation query.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Load test `GET /api/v2/sbom/{id}/advisory-summary` against an SBOM with 500 linked advisories and assert p95 < 200ms on cache misses (cold cache, or cache invalidated between requests)
- [ ] Load test the same endpoint on cache hits and record p95 for comparison
- [ ] Sustained load run (for example, 30 minutes at a steady request rate across many SBOM IDs): server memory stays flat, including the cache footprint, which must stay bounded as distinct SBOM IDs grow
- [ ] Data-volume scaling: benchmark the aggregation query at 50, 500, and 5,000 advisories per SBOM, and with a large total `sbom_advisory` table, then confirm that latency grows sub-linearly and that the query plan (`EXPLAIN ANALYZE`) uses indexes on the join table rather than sequential scans
- [ ] Concurrency: benchmark the summary endpoint while advisory ingestion runs concurrently and confirm that invalidation does not cause latency spikes above the 500ms alert threshold
- [ ] Compare against the baseline of fetching all pages of `GET /api/v2/sbom/{id}/advisories` for the same SBOM and record the improvement

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service aggregation
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Invalidate cached advisory summaries on advisory ingestion
- Depends on: Task 4 — Add optional threshold query parameter
