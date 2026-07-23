## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM. Without this, the 5-minute cached response from `GET /api/v2/sbom/{id}/advisory-summary` could serve stale severity counts after new advisories are ingested and correlated. The ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` must evict or invalidate the cache entry for any SBOM that gains a new advisory link.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after new advisory-SBOM correlations are stored. When a new advisory is linked to an SBOM (via the `sbom_advisory` join table), invalidate the cached advisory-summary for that SBOM.

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. Locate the code path where new `sbom_advisory` join records are inserted and add a cache invalidation call after the insert.
- Per Key Conventions §Caching: the project uses `tower-http` caching middleware. Determine the cache invalidation mechanism used by the project (e.g., cache key eviction via a shared cache handle, or tag-based invalidation). Follow the pattern established by any existing cache invalidation in the codebase.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust source file scope.
- Per Key Conventions §Error handling: wrap cache invalidation calls with `.context("invalidate advisory-summary cache")` for proper error reporting. Cache invalidation failures should be logged but not block ingestion — use a warn-and-continue pattern rather than returning an error.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust source file scope.
- The cache key should be derived from the SBOM ID to enable targeted invalidation rather than flushing the entire cache.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion correlation logic; the insertion point for the invalidation hook
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module; may contain existing cache invalidation patterns to follow
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — the endpoint that sets up the cache (from Task 2); reference for the cache key structure

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM during ingestion, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` requests after ingestion return updated severity counts
- [ ] Cache invalidation failures are logged as warnings but do not block the ingestion pipeline
- [ ] Cache invalidation is targeted to the specific SBOM (not a full cache flush)

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, then verify that `GET /api/v2/sbom/{id}/advisory-summary` returns updated counts (not stale cached response)
- [ ] Integration test: verify that cache invalidation for one SBOM does not affect the cached summary of a different SBOM

## Dependencies
- Depends on: Task 2 — Add advisory-summary endpoint with caching
