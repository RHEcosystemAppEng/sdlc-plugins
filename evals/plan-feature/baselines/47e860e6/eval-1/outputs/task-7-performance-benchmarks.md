**Summary**: Performance benchmarks for advisory severity aggregation

## Repository
trustify-backend

## Target Branch
main

## Description
Cross-cutting **Performance Benchmarks** validation for Feature TC-9001, derived from the repository's testing readiness template (`docs/testing-readiness.md`, category "Performance Benchmarks"). Validate the feature's NFR — p95 < 200ms for SBOMs with up to 500 advisories — and confirm no memory leaks or query degradation as data volume grows.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Load test `GET /api/v2/sbom/{id}/advisory-summary` against an SBOM with 500 correlated advisories: p95 < 200ms on a cold cache (cache invalidated / disabled) and on a warm cache
- [ ] Sustained load test (e.g. 30 minutes) shows stable process memory, including the summary cache (entries expire after 5 minutes and do not grow unbounded across many SBOM IDs)
- [ ] Compare latency for SBOMs with 50, 500, and 5,000 advisories and for databases with increasing total SBOM/advisory counts; inspect `EXPLAIN ANALYZE` for the aggregation query to confirm index use on `sbom_advisory` (no sequential scan growth)
- [ ] Measure under concurrent advisory ingestion (cache invalidations) to confirm latency remains within threshold
- [ ] Record results against the ~2s baseline of the current multi-page client-side approach

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and SBOM aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache
- Depends on: Task 3 — Invalidate cached advisory summaries on advisory ingestion
- Depends on: Task 4 — Support optional threshold query parameter on advisory-summary (non-MVP)
