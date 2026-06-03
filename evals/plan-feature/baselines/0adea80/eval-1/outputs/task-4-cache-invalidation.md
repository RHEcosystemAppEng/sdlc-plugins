# Task 4 — Add cache invalidation for advisory summary on advisory ingestion

## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, any cached advisory summary for that SBOM is invalidated. This ensures the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns fresh data after new advisories are ingested, fulfilling the non-functional requirement for cache consistency.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation step

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. The correlation step is where advisories are linked to SBOMs. After this step completes, the cached advisory summary for the affected SBOM(s) must be invalidated.
- Investigate the existing `tower-http` caching setup to determine how cache entries are keyed and how to programmatically invalidate them. The cache key is likely based on the request path (`/api/v2/sbom/{id}/advisory-summary`), so invalidation should target entries matching the affected SBOM ID(s).
- If `tower-http`'s caching layer does not support programmatic invalidation, consider alternative approaches:
  - Store a cache version/generation counter per SBOM in the database and include it in cache key computation
  - Use a lightweight in-memory cache (e.g., `moka` or `mini-moka`) in the service layer instead of HTTP-level caching, which allows explicit key-based invalidation
  - Use `Cache-Control: no-cache` with ETag/Last-Modified validation instead of time-based expiry
- Reference the `IngestorService` in `modules/ingestor/src/service/mod.rs` and the advisory ingestion graph in `modules/ingestor/src/graph/advisory/mod.rs` to understand the ingestion flow and identify the exact point where advisory-SBOM links are created.
- Per docs/constraints.md Section 5 (Code Change Rules): changes must be scoped to the listed files; code must not be modified without first inspecting it; do not duplicate existing functionality.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — the existing advisory ingestion/correlation code where the invalidation hook should be placed
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion may demonstrate patterns for post-ingestion hooks or side effects
- `modules/ingestor/src/service/mod.rs::IngestorService` — the service orchestrating ingestion, may contain cache or event patterns

## Acceptance Criteria
- [ ] After advisory ingestion links a new advisory to an SBOM, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` return updated counts reflecting the newly ingested advisory
- [ ] Cache invalidation does not affect unrelated SBOM summaries
- [ ] No regression in advisory ingestion performance or correctness

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify the advisory summary endpoint reflects the new advisory without waiting for cache expiry
- [ ] Integration test: verify that ingesting an advisory for SBOM-A does not invalidate the cache for SBOM-B

## Verification Commands
- `cargo build` — full project compiles
- `cargo test --test api` — integration tests pass
- `cargo test -p trustify-module-ingestor` — ingestor tests pass

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
