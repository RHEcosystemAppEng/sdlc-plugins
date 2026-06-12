# Task 4 — Add cache invalidation for advisory summary on advisory ingestion

## Repository
trustify-backend

## Target Branch
main

## Description
Modify the advisory ingestion pipeline to invalidate cached advisory summaries when new advisories are linked to an SBOM. This ensures that the 5-minute cache on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint does not serve stale data after new advisory-SBOM correlations are established during ingestion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation is established during advisory ingestion

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. After the correlation step (where advisories are linked to SBOMs via the `sbom_advisory` join table), add a cache invalidation call.
- Follow the existing `tower-http` caching pattern used in the repository. The cache invalidation mechanism depends on how the cache layer is configured:
  - If using in-memory cache (e.g., `tower-http`'s built-in cache), invalidate by cache key pattern matching the SBOM ID(s) affected by the newly ingested advisory.
  - If using an external cache layer, call the appropriate invalidation API.
- Identify the specific SBOM IDs affected by the advisory correlation and invalidate only those cache entries, not the entire cache. This is important for performance.
- The ingestion pipeline in `modules/ingestor/src/service/mod.rs` (`IngestorService`) orchestrates the ingestion flow — review it to understand the call chain and find the optimal insertion point for cache invalidation.
- Error handling: cache invalidation failures should be logged as warnings but should NOT fail the advisory ingestion transaction. Ingestion correctness is more important than cache freshness.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion and correlation logic where invalidation will be added
- `modules/ingestor/src/service/mod.rs::IngestorService` — orchestrator service showing the ingestion flow

## Acceptance Criteria
- [ ] After advisory ingestion links a new advisory to an SBOM, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` calls after ingestion return updated counts
- [ ] Cache invalidation failure does not cause advisory ingestion to fail
- [ ] Only the affected SBOM cache entries are invalidated, not the entire cache

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify that the advisory-summary endpoint reflects the new advisory count
- [ ] Test that cache invalidation errors are handled gracefully (logged but not propagated)

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
