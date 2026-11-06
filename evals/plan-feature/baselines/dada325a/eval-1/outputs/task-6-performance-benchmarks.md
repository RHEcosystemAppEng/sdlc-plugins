## Repository
trustify-backend

## Target Branch
main

## Description
Run feature-level performance benchmarks for TC-9001 ("Add advisory severity aggregation endpoint"), following the **Performance Benchmarks** category of the repository's testing readiness template (`docs/testing-readiness.md`). The goal is to validate the Feature's non-functional requirement: p95 response time under 200ms for SBOMs with up to 500 advisories, compared with ~2s for today's multi-page client-side approach. The benchmarks must also show that sustained use of the endpoint and its cache does not leak memory, and that the aggregation query does not degrade as data volume grows.

Readiness template acceptance criteria covered by this task:
- API response time is within acceptable thresholds under load
- No memory leaks detected during sustained usage
- Database query performance does not degrade with increased data volume

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Load test `GET /api/v2/sbom/{id}/advisory-summary` against an SBOM with 500 linked advisories. p95 latency is under 200ms on both cold-cache (first request) and warm-cache requests.
- [ ] Load test with concurrent requests across many distinct SBOM IDs. p95 stays under 200ms, and no request exceeds the 500ms alerting threshold named in the Feature.
- [ ] Sustained load (e.g., 30+ minutes) across a large and growing set of SBOM IDs. Process memory stabilizes: cache entries expire after the 5-minute TTL, and the cache does not grow without bound.
- [ ] Sustained load with concurrent advisory ingestion (triggering cache invalidation). No memory growth and no latency regression.
- [ ] Run the aggregation query (EXPLAIN ANALYZE) against datasets of increasing size: 10, 100, and 500 advisories per SBOM, and a large total number of SBOMs. Query time grows sub-linearly or stays within budget, and the plan uses the existing indexes on the `sbom_advisory` join table (no sequential scan of the full table).
- [ ] Record benchmark results (p50/p95/p99, memory profile, query plans) in the task's Jira comment for traceability

## Dependencies
- Depends on: Task 1 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
- Depends on: Task 2 — Cache advisory summary for 5 minutes with ingestion-driven invalidation
- Depends on: Task 3 — Add optional threshold filter to advisory summary endpoint
