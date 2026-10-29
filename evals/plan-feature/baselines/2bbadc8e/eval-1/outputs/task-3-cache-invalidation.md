## Repository
trustify-backend

## Target Branch
main

## Description
Modify the advisory ingestion pipeline to invalidate cached advisory-summary responses when new advisories are linked to an SBOM. Without cache invalidation, the 5-minute cache on the advisory-summary endpoint could serve stale severity counts after new advisory data is ingested. This task ensures that severity counts remain accurate immediately after advisory ingestion completes.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation after advisory-to-SBOM correlation step
- `modules/ingestor/src/service/mod.rs` — inject cache handle into IngestorService if needed for cache key invalidation

## Implementation Notes
- The advisory ingestion module (`modules/ingestor/src/graph/advisory/mod.rs`) parses, stores, and correlates advisories to SBOMs. After the correlation step links a new advisory to an SBOM, invalidate the cache entry for that SBOM's advisory-summary endpoint.
- Determine the cache architecture from Task 2's implementation: if the cache layer uses a shared in-memory store (e.g., a concurrent HashMap or LRU cache), inject the cache handle into the ingestion service so it can invalidate specific keys by SBOM ID. If the cache is HTTP-level only (tower-http response cache), consider using cache tags, ETag-based invalidation, or a cache-busting version counter.
- The cache invalidation must target only the affected SBOM's summary cache entry, not all cached summaries globally.
- Fail-closed behavior for the invalidation itself: if the cache invalidation call fails (e.g., cache store is temporarily unavailable), log an error at WARN level but do not fail the advisory ingestion operation. The stale cache entry will expire naturally after the 5-minute TTL. This is acceptable because serving slightly stale counts for up to 5 minutes is preferable to failing advisory ingestion entirely.
- Per CONVENTIONS.md §Error Handling: use `.context()` wrapping for error propagation in the ingestion pipeline. See `common/src/error.rs` for the `AppError` enum.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's .rs handler scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion flow; extend the correlation step with cache invalidation
- `modules/ingestor/src/service/mod.rs::IngestorService` — service where the cache handle may need to be injected
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — cache configuration from Task 2 that defines what cache keys need invalidating

## Acceptance Criteria
- [ ] After advisory ingestion correlates a new advisory to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` requests after ingestion return updated severity counts reflecting the newly ingested advisory
- [ ] Cache invalidation failure does not cause advisory ingestion to fail — errors are logged at WARN level and ingestion continues
- [ ] Cache invalidation targets only the affected SBOM's summary cache entry, not all cached summaries

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to a known SBOM, then query advisory-summary and verify the response includes the new advisory in the severity counts
- [ ] Test that cache invalidation failure (simulated) is logged but does not prevent advisory ingestion from completing successfully
- [ ] Test that unrelated SBOM advisory-summary cache entries remain cached after invalidation of a specific SBOM's cache

## Verification Commands
- `cargo build -p trustify-ingestor` — compiles without errors
- `cargo test -p trustify-ingestor` — all tests pass

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
