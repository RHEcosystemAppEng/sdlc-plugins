## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory summaries are invalidated when new advisories are linked to an SBOM. Without this, the 5-minute cache from the advisory-summary endpoint (Task 2) could serve stale severity counts after new advisories are ingested. The ingestion pipeline must invalidate the cached summary for each SBOM affected by the newly ingested advisory.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- add cache invalidation call after advisory-to-SBOM correlation completes; invalidate the advisory-summary cache entry for each affected SBOM ID

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles advisory parsing, storage, and correlation with SBOMs. After the correlation step links an advisory to SBOMs, add a cache invalidation call for each affected SBOM ID.
- The cache invalidation mechanism depends on how the tower-http cache layer is configured in Task 2. Common approaches include: (1) using a shared cache store with explicit key eviction, or (2) using cache tags or a generation counter that the endpoint checks. Follow whichever pattern is established by Task 2's cache configuration.
- Identify the exact location in the ingestion flow where advisory-SBOM links are created. The `entity/src/sbom_advisory.rs` join table entity is inserted during this step -- place the invalidation call immediately after successful insertion.
- Per CONVENTIONS.md §Error Handling: wrap any cache invalidation errors with `.context()` and handle them gracefully -- cache invalidation failure should log a warning but not fail the ingestion pipeline. See `modules/ingestor/src/graph/advisory/mod.rs` for existing error handling patterns. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust service file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` -- existing advisory ingestion flow showing where SBOM-advisory links are created
- `entity/src/sbom_advisory.rs` -- the SBOM-Advisory join table entity whose insertion triggers cache invalidation

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent calls to GET /api/v2/sbom/{id}/advisory-summary after ingestion return updated severity counts
- [ ] Cache invalidation failures are logged as warnings but do not fail the ingestion pipeline
- [ ] Cache invalidation targets only the affected SBOM IDs, not the entire cache

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify the advisory-summary endpoint returns updated counts after ingestion
- [ ] Integration test: verify that cache invalidation for one SBOM does not affect cached summaries for other SBOMs
- [ ] Unit test: verify that a cache invalidation error is logged as a warning but does not propagate as an error

## Dependencies
- Depends on: Task 2 -- Add advisory-summary endpoint with caching
