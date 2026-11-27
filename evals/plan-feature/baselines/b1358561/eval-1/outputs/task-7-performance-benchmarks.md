Summary: Performance benchmarks for advisory severity aggregation
Epic: TC-9001: Documentation and feature validation
Labels: ai-generated-jira | Priority: Major | Fix Version: RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Cross-cutting **Performance Benchmarks** validation for Feature TC-9001 (Add advisory
severity aggregation endpoint), derived from the "Performance Benchmarks" category of the
repository's testing readiness template (`docs/testing-readiness.md`). The Feature's NFR sets
the threshold: p95 < 200ms for SBOMs with up to 500 advisories (goal: reduce summary load from
~2s multi-page fetch to <200ms single call). Validate response time under load, absence of
memory leaks (including in the response cache), and that the aggregation query does not
degrade as data volume grows.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Load test `GET /api/v2/sbom/{id}/advisory-summary` for an SBOM with 500 correlated advisories: p95 < 200ms on cache miss (cold) and measured on cache hit (warm)
- [ ] Load test with concurrent requests across many distinct SBOM IDs: p95 remains < 200ms
- [ ] Sustained load run (e.g., 30+ minutes across many SBOM IDs with ongoing advisory ingestion triggering invalidation): process memory stabilizes; cache size is bounded by TTL/eviction
- [ ] Measure aggregation query time with `EXPLAIN ANALYZE` for SBOMs with 50, 500, and 5,000 advisories and with a large total `sbom_advisory` table; confirm index use on the SBOM ID join column and no sequential scans of the full join table
- [ ] Compare against baseline: multi-page `GET /api/v2/sbom/{id}/advisories` fetch + client-side count for the same SBOM, documenting the improvement

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute caching
- Depends on: Task 3 — Invalidate cached advisory summaries on advisory and SBOM ingestion
- Depends on: Task 4 — Support optional ?threshold query parameter on advisory-summary
