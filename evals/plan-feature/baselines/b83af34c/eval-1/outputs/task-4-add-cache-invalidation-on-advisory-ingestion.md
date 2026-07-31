## Repository
trustify-backend

## Target Branch
main

## Priority
Major

## Fix Versions
RHTPA 1.5.0

## Description
Modify the advisory ingestion pipeline to invalidate cached advisory summary responses when new advisories are linked to an SBOM. This ensures that the 5-minute cache for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint is proactively cleared when advisory data changes, so consumers always see up-to-date severity counts after ingestion completes.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation completes

## Implementation Notes
In `modules/ingestor/src/graph/advisory/mod.rs`, the advisory ingestion flow correlates advisories with SBOMs. After the correlation step links a new advisory to one or more SBOMs, add a cache invalidation call that clears the cached advisory-summary response for each affected SBOM ID.

The specific invalidation mechanism depends on how the `tower-http` caching layer stores entries. If using an in-memory cache (e.g., via a shared `Arc<Cache>`), call the cache's `invalidate` or `remove` method with the cache key corresponding to `/api/v2/sbom/{id}/advisory-summary`. If using HTTP-level cache headers only, no server-side invalidation is needed — the 5-minute TTL will naturally expire. Determine the approach by examining the caching setup added in Task 3.

Follow the existing ingestion pipeline patterns in `modules/ingestor/src/graph/sbom/mod.rs` for post-processing hooks.

Per CONVENTIONS.md §Framework: use SeaORM transaction context available in the ingestion pipeline. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust syntax scope.

Per CONVENTIONS.md §Module pattern: modify within the existing `graph/advisory/` module structure. Applies: convention has no file-type restriction (broadly applicable).

Per CONVENTIONS.md §Error handling: wrap cache invalidation errors with `.context()` and propagate as `AppError`. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust syntax scope.

Per CONVENTIONS.md §Caching: invalidate `tower-http` cached entries for affected SBOM advisory summaries after ingestion. Applies: convention has no file-type restriction (broadly applicable).

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module for pattern reference on post-processing hooks
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion flow to extend

## Acceptance Criteria
- [ ] Cache invalidation is triggered when new advisories are linked to SBOMs during ingestion
- [ ] Only cache entries for affected SBOM IDs are invalidated (not a full cache flush)
- [ ] Advisory ingestion still completes successfully after adding invalidation logic
- [ ] Cache invalidation errors are logged but do not fail the ingestion pipeline

## Test Requirements
- [ ] Verify that after ingesting a new advisory linked to an SBOM, the next call to `GET /api/v2/sbom/{id}/advisory-summary` reflects the updated counts (not stale cached data)
- [ ] Verify that advisory ingestion does not fail if cache invalidation encounters an error

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching
