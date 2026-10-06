## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are cleared when new advisories are linked to an SBOM. Without this, the `/advisory-summary` endpoint could serve stale severity counts for up to 5 minutes after new advisories are ingested.

The advisory ingestion pipeline (in the ingestor module) already correlates advisories with SBOMs. After the correlation step, the pipeline must invalidate any cached advisory-summary for the affected SBOM IDs.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation step

## Implementation Notes
- Locate the advisory ingestion and correlation logic in `modules/ingestor/src/graph/advisory/mod.rs`. This module parses advisories, stores them, and correlates them with SBOMs.
- After the correlation step that links an advisory to one or more SBOMs, add a cache invalidation call for each affected SBOM's advisory-summary cache key.
- The cache invalidation mechanism depends on the tower-http caching middleware configuration. If it uses an in-memory cache, clear the relevant entries by key pattern (e.g., `/api/v2/sbom/{id}/advisory-summary`). If it uses an external cache (Redis, etc.), make the appropriate invalidation call.
- If the caching middleware does not support targeted key invalidation, consider an alternative approach: use a version counter or ETag that increments when advisory data changes for an SBOM, causing the cache to miss on the next request.
- Per repo conventions: error handling uses `Result<T, AppError>` with `.context()` wrapping.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion logic where the invalidation hook should be added
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module; reference for how the ingestion pipeline is structured

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM via the ingestion pipeline, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` calls after advisory ingestion return updated severity counts
- [ ] Cache invalidation does not cause errors when no cached entry exists for the SBOM

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, then verify that the advisory-summary endpoint reflects the new advisory in its counts
- [ ] Test: cache invalidation for a non-cached SBOM does not produce errors

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache
