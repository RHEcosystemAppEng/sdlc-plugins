## Repository
trustify-backend

## Target Branch
main

## Description
Run the **Performance Benchmarks** category from the repository's testing readiness template (`docs/testing-readiness.md`) against the advisory severity aggregation feature (TC-9001). Validate the feature's non-functional target: p95 < 200ms for `GET /api/v2/sbom/{id}/advisory-summary` on SBOMs with up to 500 advisories. Also confirm there are no memory leaks under sustained load and that the aggregation query does not degrade as data volume grows.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Load test `GET /api/v2/sbom/{id}/advisory-summary` for an SBOM with 500 linked advisories. p95 < 200ms on both cache-miss (first request, or after invalidation) and cache-hit paths, measured separately.
- [ ] Load test under concurrent requests across many distinct SBOM IDs (low cache-hit ratio). p95 stays < 200ms and never exceeds the 500ms alert threshold.
- [ ] Sustained load (e.g., 30+ minutes) with interleaved advisory ingestion triggering cache invalidation. Server memory stays stable with no unbounded cache growth.
- [ ] Query scaling: measure cache-miss latency for SBOMs with 50, 200, and 500 advisories, and with a large total `sbom_advisory` table. Latency grows sub-linearly, and `EXPLAIN ANALYZE` shows index use on the join (no full-table scans).
- [ ] Compare against the baseline (multi-page fetch of `GET /api/v2/sbom/{id}/advisories`, ~2s) to confirm the improvement goal

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service aggregation
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Invalidate cached advisory summaries on advisory/SBOM ingestion
- Depends on: Task 4 — Support ?threshold query parameter on advisory-summary endpoint (non-MVP)
