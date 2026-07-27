# Task 4 — Add cache invalidation for advisory-summary on advisory ingestion

## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM. Without this, the 5-minute cache on the advisory-summary endpoint could serve stale data after new advisories are ingested, leading to incorrect severity counts in dashboards and alerting integrations.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation completes; invalidate the advisory-summary cache entry for the affected SBOM ID(s)

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. The cache invalidation hook should be placed after the correlation step completes (i.e., after the `sbom_advisory` join records are written).
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust ingestion module scope.
- The caching layer uses `tower-http` middleware. Determine the cache invalidation mechanism available: `tower-http` cache layers typically support either key-based eviction or TTL-based expiry. If the cache implementation supports explicit key eviction, invalidate the cache entry for the specific SBOM ID. If only TTL-based expiry is available, consider reducing the TTL or using a cache-busting mechanism.
- The `IngestorService` at `modules/ingestor/src/service/mod.rs` orchestrates ingestion — check if cache access is already available in the service context or if a cache handle needs to be injected.
- Error handling: cache invalidation failures should be logged but not fail the ingestion pipeline. Use `.context("failed to invalidate advisory-summary cache")` for error wrapping, but catch and log rather than propagate.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion module; the cache invalidation hook is added to this module's correlation step
- `modules/ingestor/src/service/mod.rs::IngestorService` — orchestrates ingestion; may already hold references to shared state that includes cache handles

## Acceptance Criteria
- [ ] Advisory-summary cache is invalidated for the affected SBOM when new advisories are linked via ingestion
- [ ] Cache invalidation does not block or fail the advisory ingestion pipeline
- [ ] Subsequent requests to `GET /api/v2/sbom/{id}/advisory-summary` return updated counts after ingestion completes
- [ ] Cache invalidation failures are logged as warnings, not errors

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify that the advisory-summary endpoint returns updated counts (not stale cached values)
- [ ] Integration test: cache invalidation failure does not prevent advisory ingestion from completing

## Verification Commands
- `cargo build -p ingestor` — compiles without errors
- `cargo test -p ingestor -- advisory` — ingestion tests pass
- `cargo test --test api -- advisory_summary` — integration tests pass with cache invalidation

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
