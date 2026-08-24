## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation for the advisory-summary endpoint responses when new advisories are ingested and linked to SBOMs. The advisory ingestion pipeline must invalidate cached advisory-summary responses for any SBOM that gains new advisory links, ensuring that stale counts are never served after new vulnerability data arrives.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation completes

## Implementation Notes
- Per CONVENTIONS.md §Error Handling: wrap cache invalidation errors with `.context()` and propagate as `AppError` rather than silently swallowing failures.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust handler scope.
- After the advisory ingestion correlates advisories with SBOMs (linking entries in the `sbom_advisory` join table), invalidate the cached advisory-summary response for each affected SBOM ID.
- Determine the cache invalidation mechanism used by the existing `tower-http` caching middleware — if it supports key-based invalidation, invalidate by the SBOM-specific cache key. If not, a broader cache clear may be necessary.
- The invalidation must happen within the same transaction or immediately after the advisory-SBOM link is persisted, to prevent a race condition where the cache is read between the link insert and the invalidation.
- Reference `modules/ingestor/src/graph/sbom/mod.rs` for the SBOM ingestion pattern to understand how the ingestion pipeline is structured.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module; reference for ingestion pipeline structure and post-processing hooks
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table; identifies which SBOMs are affected when an advisory is ingested

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` calls after ingestion return updated counts
- [ ] Cache invalidation errors are logged and propagated, not silently swallowed
- [ ] Cache invalidation does not introduce significant latency to the advisory ingestion pipeline

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify that a subsequent advisory-summary call reflects the new advisory
- [ ] Integration test: verify that advisory-summary for an unrelated SBOM is not affected by ingestion for a different SBOM
- [ ] Verify cache invalidation error handling by simulating a cache failure

## Verification Commands
- `cargo test --package trustify-ingestor -- graph::advisory::tests::cache_invalidation` — verify cache invalidation tests pass
- `cargo check --package trustify-ingestor` — verify compilation

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
