## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory summary responses are cleared when new advisories are linked to an SBOM. Without invalidation, stale severity counts would persist for up to 5 minutes after new advisory data is ingested, potentially misleading dashboard consumers and alerting integrations.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation completes, targeting the advisory summary cache entries for all affected SBOM IDs

## Implementation Notes
The advisory ingestion process in `modules/ingestor/src/graph/advisory/mod.rs` parses advisory data and correlates it with SBOMs by creating entries in the `sbom_advisory` join table. After the correlation step completes, identify all SBOM IDs that were linked to the newly ingested advisory and invalidate their cached advisory summary responses.

The invalidation mechanism depends on the `tower-http` caching layer's implementation. If the cache supports key-based invalidation, invalidate by the SBOM-specific cache key. If the cache is a global time-based cache without key-level control, consider using a cache-busting version counter stored alongside the SBOM entity or in an in-memory cache map.

Ensure the invalidation is performed inside the same transaction as the advisory ingestion (if possible) to prevent race conditions where a request between ingestion and invalidation would cache stale data.

Per CONVENTIONS.md §Error Handling: wrap any cache invalidation errors with `.context("advisory summary cache invalidation")` and log them without failing the ingestion pipeline — cache invalidation is best-effort.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion and correlation logic where the invalidation hook will be added
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module for reference on how ingestion pipelines are structured and how cross-cutting concerns are handled

## Acceptance Criteria
- [ ] After ingesting a new advisory that links to an SBOM, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` calls after ingestion return updated counts reflecting the new advisory
- [ ] Cache invalidation failures are logged but do not fail the advisory ingestion pipeline
- [ ] Cache invalidation covers all SBOM IDs affected by the newly ingested advisory

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, verify the advisory summary endpoint returns updated counts without waiting for cache TTL expiration
- [ ] Integration test: verify advisory ingestion still succeeds even if cache invalidation encounters an error

## Verification Commands
- `cargo check -p trustify-ingestor` — compiles without errors
- `cargo test -p trustify-ingestor advisory_cache` — cache invalidation tests pass

## Dependencies
- Depends on: Task 3 — Add advisory summary REST endpoint with caching
