# Task 4 -- Add cache invalidation for advisory summaries

## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory summary for that SBOM is invalidated. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint always returns up-to-date severity counts after new advisory data is ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- add cache invalidation call after advisory-to-SBOM correlation completes
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- ensure the cache layer for the advisory-summary route supports programmatic invalidation (may need to switch from `tower-http` default to a cache key strategy that allows targeted invalidation by SBOM ID)

## Implementation Notes
- Inspect `modules/ingestor/src/graph/advisory/mod.rs` to understand the advisory ingestion flow. The key moment to invalidate is after the advisory is correlated (linked) to an SBOM in the `sbom_advisory` table.
- **Cache invalidation strategy**: The approach depends on the existing cache infrastructure. Common patterns:
  1. If using an in-memory cache with key-based lookup (e.g., `moka`, `dashmap`), add a cache eviction call using the SBOM ID as the cache key after the SBOM-advisory link is inserted.
  2. If using `tower-http` response caching, the cache is HTTP-level and may not support targeted invalidation. In this case, consider adding an application-level cache (e.g., `moka::sync::Cache`) in the service layer with a TTL of 5 minutes, and invalidate by SBOM ID key from the ingestor.
  3. If the project uses a shared cache (e.g., Redis), add a cache delete call.
- Check how other parts of the codebase handle cache invalidation to follow the established pattern. Search for cache eviction or invalidation calls in the ingestor module.
- The ingestor and fundamental modules will need a shared reference to the cache instance. This is typically done through the Axum application state or a shared service container.
- **Non-functional requirement**: No new database tables. The cache must be in-memory or use an existing external cache.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` -- advisory ingestion and correlation flow; this is where the invalidation hook must be placed
- `modules/ingestor/src/graph/sbom/mod.rs` -- SBOM ingestion flow; reference for how the ingestor interacts with shared state and services

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts
- [ ] No new database tables are introduced

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify that the advisory-summary endpoint reflects the new advisory (cache is invalidated)
- [ ] Integration test: verify that cached summaries for unrelated SBOMs are NOT invalidated when a new advisory is linked to a different SBOM

## Verification Commands
- `cargo test --package ingestor -- test_advisory_cache_invalidation` -- cache invalidation tests pass

## Dependencies
- Depends on: Task 3 -- Add GET /api/v2/sbom/{id}/advisory-summary endpoint
