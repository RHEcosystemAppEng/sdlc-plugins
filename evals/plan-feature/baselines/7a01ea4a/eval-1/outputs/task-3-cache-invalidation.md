## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory summary responses are invalidated when new advisories are linked to an SBOM. Without this, the `GET /api/v2/sbom/{id}/advisory-summary` endpoint could serve stale severity counts for up to 5 minutes after new advisories are correlated. The invalidation must target only the affected SBOM's cached summary, not the entire cache.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation step to invalidate the advisory summary cache for affected SBOMs

## Implementation Notes
- The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. Locate the step where advisory-SBOM links are created (the correlation step) and add cache invalidation after it.
- The `tower-http` caching middleware used by the endpoint (Task 2) manages cache entries. Invalidation should target the specific cache key for the affected SBOM's advisory summary. Inspect how the existing caching infrastructure exposes invalidation hooks or cache key management.
- If `tower-http` does not support targeted invalidation, consider using a shared cache store (e.g., an in-memory cache behind an `Arc<RwLock<>>`) that the ingestion pipeline can access. This approach is common in Axum applications where middleware-level caching needs programmatic invalidation.
- Per Key Conventions (Module pattern): each domain module uses `model/ + service/ + endpoints/` structure — the ingestion module follows `graph/` structure instead but uses the same error handling patterns.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion pipeline where the cache invalidation hook must be added
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pipeline that may demonstrate existing cache or state invalidation patterns

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` return updated severity counts after advisory ingestion
- [ ] Cache invalidation targets only the affected SBOM, not the entire cache

## Test Requirements
- [ ] Integration test: ingest an advisory for an SBOM, verify the summary endpoint returns updated counts (not stale cached data)
- [ ] Integration test: ingesting an advisory for SBOM A does not invalidate the cache for SBOM B

## Verification Commands
- `cargo test --test api cache_invalidation` — cache invalidation tests pass

## Dependencies
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
