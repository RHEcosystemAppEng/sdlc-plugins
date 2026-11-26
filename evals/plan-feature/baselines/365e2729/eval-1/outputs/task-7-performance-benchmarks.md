## Repository
trustify-backend

## Target Branch
main

## Description
Run feature-level performance benchmarks for TC-9001 (advisory severity aggregation endpoint) per the "Performance Benchmarks" category of the repository's testing readiness template (`docs/testing-readiness.md`). The Feature's non-functional requirement is p95 < 200ms for SBOMs with up to 500 advisories (goal: reduce summary load time from ~2s multi-page fetch to <200ms single call). Validate response time under load, absence of memory leaks under sustained usage (including the response cache), and that the aggregation query does not degrade as data volume grows.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Load test `GET /api/v2/sbom/{id}/advisory-summary` against an SBOM with 500 linked advisories: p95 latency < 200ms with cold cache (uncached aggregation path) and with warm cache
- [ ] Load test with `?threshold=critical` meets the same p95 < 200ms threshold
- [ ] Sustained-load run (e.g., 30+ minutes across many distinct SBOM IDs) shows stable process memory, confirming cached entries expire after 5 minutes and do not accumulate unbounded
- [ ] Benchmark the aggregation query at increasing data volumes (e.g., 50, 500, 5,000 advisories per SBOM and growing total `sbom_advisory` row counts); confirm the query plan uses indexes on the join table and latency scales acceptably
- [ ] Record results in the Jira task so they can be compared against the Grafana latency dashboard baseline

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Invalidate advisory-summary cache on advisory ingestion
- Depends on: Task 4 — Add optional severity threshold filter to advisory-summary endpoint
