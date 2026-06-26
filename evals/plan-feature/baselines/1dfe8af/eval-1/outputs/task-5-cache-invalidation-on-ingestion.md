## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM. Without this, the severity counts would serve stale data for up to 5 minutes after new advisories are ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after advisory-SBOM correlation completes

## Implementation Notes
Modify the advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` to invalidate the advisory-summary cache after new advisories are correlated with SBOMs.

The ingestion flow in `modules/ingestor/src/graph/advisory/mod.rs` parses advisories, stores them, and then correlates them with affected SBOMs. After the correlation step, identify which SBOM IDs were affected and invalidate their cache entries.

The invalidation approach depends on the caching mechanism used in Task 4:
- If using application-level in-memory cache: call a cache eviction method for each affected SBOM ID
- If using HTTP-level Cache-Control headers: no server-side invalidation is possible; consider switching to application-level caching or accepting stale data until TTL expires

The ingestor module (`modules/ingestor/Cargo.toml`) may need a dependency on the cache service if it doesn't already have one.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Existing advisory ingestion logic; the correlation step identifies affected SBOM IDs
- `modules/ingestor/src/service/mod.rs::IngestorService` — Service layer that may coordinate cache access

## Acceptance Criteria
- [ ] Advisory ingestion invalidates cached advisory-summary for all affected SBOM IDs
- [ ] New advisory-summary requests after ingestion return updated counts
- [ ] Invalidation only clears cache entries for SBOMs affected by the ingested advisories, not all entries
- [ ] No regression in advisory ingestion latency (invalidation should be lightweight)

## Test Requirements
- [ ] Integration test: ingest an advisory, verify cached summary is refreshed with new counts
- [ ] Test that cache for unrelated SBOMs is not invalidated

## Verification Commands
- `cargo check -p trustify-ingestor` — compiles without errors

## Dependencies
- Depends on: Task 4 — Endpoint caching

[sdlc-workflow] Description digest: sha256-md:e8a1b3c5d7f9402917c53e8f9b2d6f0a1e34a5b7c9d1423e5f7a9b1c3d4e6f8
