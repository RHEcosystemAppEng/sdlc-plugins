## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory severity summaries are invalidated when new advisories are linked to an SBOM. Without this, the `GET /api/v2/sbom/{id}/advisory-summary` endpoint could serve stale severity counts for up to 5 minutes after new advisory data is ingested. The advisory ingestion code in `modules/ingestor/src/graph/advisory/mod.rs` must invalidate the cache entry for each SBOM that is affected by a newly ingested advisory, as specified in TC-9001's non-functional requirements.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation calls after advisory-to-SBOM correlation completes, targeting the advisory summary cache entries for each affected SBOM ID

## Implementation Notes
Per CONVENTIONS.md §Error handling: any cache invalidation errors should be handled gracefully with `.context()` wrapping and should not cause the advisory ingestion to fail. Cache invalidation is best-effort — a missed invalidation results in at most 5 minutes of stale data, which is acceptable.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` file scope.

The cache invalidation should happen after the advisory-to-SBOM linkage is persisted in the database. Identify the point in the advisory ingestion flow where `sbom_advisory` records are created or updated, and add invalidation logic after that step.

The invalidation mechanism depends on the caching layer used by tower-http. If the caching middleware uses an in-process cache (e.g., `moka` or similar), inject a cache handle into the ingestor and call `invalidate` with the cache key for each affected SBOM's advisory-summary endpoint. If HTTP-level caching is used, consider cache-busting headers or a shared cache store.

Review the existing advisory ingestion flow in `modules/ingestor/src/graph/advisory/mod.rs` to understand the correlation step where advisories are linked to SBOMs via the `sbom_advisory` join table.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Existing advisory ingestion and correlation logic; the invalidation should be added after the existing SBOM-advisory linking step
- `entity/src/sbom_advisory.rs::SbomAdvisory` — The join table entity used during advisory-SBOM correlation; the affected SBOM IDs can be extracted from the records being created

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached advisory summary for that SBOM is invalidated
- [ ] Cache invalidation covers all SBOMs affected by a single advisory ingestion (an advisory may link to multiple SBOMs)
- [ ] Cache invalidation failures do not cause advisory ingestion to fail
- [ ] After cache invalidation, the next call to `GET /api/v2/sbom/{id}/advisory-summary` returns fresh data reflecting the newly ingested advisory

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify the advisory summary endpoint reflects the new advisory without waiting for cache expiry
- [ ] Integration test: cache invalidation failure does not block advisory ingestion completion
- [ ] Unit test: verify that invalidation is called for each affected SBOM ID during advisory ingestion

## Verification Commands
- `cargo build -p trustify-ingestor` — Compiles without errors
- `cargo test -p trustify-ingestor -- cache_invalidation` — Cache invalidation tests pass

## Dependencies
- Depends on: Task 2 — Add advisory severity summary endpoint with caching and threshold filter
