# Task 7 — Performance Benchmarks for advisory severity aggregation endpoint

**Summary:** TC-9001: Performance Benchmarks — advisory severity aggregation endpoint
**Issue type:** Task
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9001)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9001)

---

## Repository
trustify-backend

## Target Branch
main

## Description
Run the feature-level performance benchmarks for TC-9001 (Add advisory severity aggregation endpoint), as defined in the "Performance Benchmarks" category of the repository's testing readiness template (`docs/testing-readiness.md`). The feature's non-functional requirement is a p95 response time under 200ms for SBOMs with up to 500 advisories (down from about 2s for the client-side multi-page fetch). Operational alerting fires when p95 exceeds 500ms. These benchmarks confirm the endpoint meets that budget under load, does not leak memory under sustained use (including the 5-minute response cache), and that the aggregation query does not slow down as data grows.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Load test `GET /api/v2/sbom/{id}/advisory-summary` against an SBOM with 500 correlated advisories. Confirm p95 < 200ms on cold-cache (uncached) requests, and report cached-response latency separately
- [ ] Load test with concurrent requests across many distinct SBOM IDs and confirm p95 stays < 200ms and never exceeds the 500ms alert threshold
- [ ] Sustained-usage test (for example 30+ minutes of continuous requests across many SBOM IDs, spanning several 5-minute cache TTL cycles, with advisory ingestion causing invalidations). Confirm process memory stabilises and the cache does not grow without bound
- [ ] Data-volume test: measure aggregation query time (`EXPLAIN ANALYZE`) at 50, 500, and 5,000 advisories per SBOM and across a database with a large total number of `sbom_advisory` rows. Confirm query time scales acceptably and uses an index on the SBOM ID column of the join table, with no sequential scan
- [ ] Compare against the baseline (multi-page `GET /api/v2/sbom/{id}/advisories` fetch-and-count) and record the improvement

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and SbomService aggregation query
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 404 handling and 5-minute caching
- Depends on: Task 3 — Invalidate cached SBOM advisory summaries from the ingestion pipeline
- Depends on: Task 4 — Add optional ?threshold= severity filter to GET /api/v2/sbom/{id}/advisory-summary
