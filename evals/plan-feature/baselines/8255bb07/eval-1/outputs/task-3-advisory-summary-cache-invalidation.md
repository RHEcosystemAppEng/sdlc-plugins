## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation for the advisory-summary endpoint's 5-minute cache in the advisory ingestion pipeline. When new advisories are linked to an SBOM during ingestion, the cached advisory-summary response for that SBOM must be invalidated so that subsequent requests return updated severity counts. This ensures data freshness after advisory correlation completes.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation completes

## Implementation Notes
- The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories to SBOMs. Locate the point where advisory-SBOM links are created (after correlation) and add cache invalidation there.
- The cache invalidation mechanism depends on the tower-http caching infrastructure used by the endpoint (Task 2). Investigate the existing caching patterns to determine the invalidation approach — this may involve clearing the cache entry by key (based on SBOM ID) or using a cache-busting strategy.
- If the caching layer does not support key-based invalidation (common with tower-http response caching), consider alternative approaches: (a) use a separate application-level cache (e.g., an in-memory HashMap with TTL) in the service layer instead of HTTP-level caching, or (b) store a version counter per SBOM that the endpoint checks against the cached version.
- Ensure invalidation is idempotent — multiple advisory ingestion events for the same SBOM should not cause errors.
- Per Key Conventions — Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — the existing advisory ingestion pipeline; the cache invalidation hook is added here after advisory-SBOM correlation
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for ingestion pipeline patterns and how post-processing hooks are structured in the ingestor module

## Acceptance Criteria
- [ ] After advisory ingestion links a new advisory to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent GET /api/v2/sbom/{id}/advisory-summary requests after ingestion return updated counts reflecting the newly linked advisory
- [ ] Cache invalidation does not affect advisory-summary caches for unrelated SBOMs
- [ ] Invalidation is idempotent — multiple ingestion events for the same SBOM do not cause errors

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify advisory-summary endpoint returns updated counts after ingestion (not stale cached data)
- [ ] Integration test: ingest an advisory for SBOM-A, verify SBOM-B's advisory-summary cache is not affected

## Verification Commands
- `cargo test --test api advisory_cache_invalidation` — run cache invalidation integration tests, expect all pass

## Dependencies
- Depends on: Task 2 — Add advisory-summary endpoint with caching and threshold filter
