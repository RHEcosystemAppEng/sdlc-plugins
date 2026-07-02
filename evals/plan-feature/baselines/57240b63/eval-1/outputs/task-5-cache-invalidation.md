## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation for advisory severity summaries in the advisory ingestion pipeline. When new advisories are linked to an SBOM during ingestion, the cached advisory summary for that SBOM must be invalidated so that subsequent requests to `GET /api/v2/sbom/{id}/advisory-summary` return fresh counts. Without this, newly ingested advisories would not appear in the summary until the 5-minute cache TTL expires naturally.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation logic after the advisory-to-SBOM correlation step; invalidate the cache entry for each affected SBOM ID when new advisory links are created

## Implementation Notes
- The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` parses, stores, and correlates advisories with SBOMs. Locate the correlation step where `sbom_advisory` join records are inserted (referencing `entity/src/sbom_advisory.rs`) — this is the trigger point for cache invalidation.
- The caching layer uses `tower-http` caching middleware (Key Conventions §Caching). Investigate how the existing cache is configured in endpoint route builders to determine the correct invalidation mechanism. Options include:
  1. **Cache-keyed invalidation**: if the tower-http cache supports programmatic eviction by key, invalidate the `/api/v2/sbom/{id}/advisory-summary` key for each affected SBOM ID.
  2. **Cache-bust header**: if programmatic eviction is not available, consider adding a version/timestamp to the cache key that gets bumped on advisory ingestion.
  3. **Shared state**: use a shared `Arc<RwLock<HashSet<Uuid>>>` of invalidated SBOM IDs that the endpoint checks before serving cached responses.
- Ensure the invalidation is scoped only to the affected SBOM IDs — do not clear the entire cache, as other endpoints' cached responses should remain valid.
- Per Key Conventions §Error handling: wrap any invalidation errors with `.context()` but do not fail the ingestion — cache invalidation is best-effort. A failed invalidation means stale data for up to 5 minutes, which is acceptable. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` ingestion file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — the existing advisory ingestion pipeline; extend it rather than creating a new module
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for ingestion patterns and how SBOM-advisory relationships are established from the SBOM side

## Acceptance Criteria
- [ ] When new advisories are linked to an SBOM during ingestion, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent requests to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts reflecting the newly linked advisories
- [ ] Cache invalidation is scoped to affected SBOM IDs only — other cached responses are unaffected
- [ ] Cache invalidation failure does not cause advisory ingestion to fail (best-effort)

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify the summary endpoint returns updated counts without waiting for cache TTL
- [ ] Integration test: verify that cache invalidation for one SBOM does not affect cached responses for other SBOMs

## Verification Commands
- `cargo check -p trustify-ingestor` — compiles without errors
- `cargo test -p trustify-tests -- advisory` — integration tests pass

## Dependencies
- Depends on: Task 3 — Implement GET /api/v2/sbom/{id}/advisory-summary endpoint with caching

## Jira Fields
- **Labels:** ai-generated-jira
- **Priority:** Major
- **Fix Versions:** RHTPA 1.5.0

[sdlc-workflow] Description digest: sha256-md:17420c55377507d92b8bfb14be0ca2587fb9f262575bae5bad4cfd345aecebe7
