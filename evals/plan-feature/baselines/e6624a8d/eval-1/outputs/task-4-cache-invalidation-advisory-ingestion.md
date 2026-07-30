## Repository
trustify-backend

## Target Branch
main

## Description
Modify the advisory ingestion pipeline to invalidate cached advisory-summary responses when new advisories are linked to an SBOM. Without this, the 5-minute cache introduced in Task 3 could serve stale severity counts after new advisories are ingested. The cache invalidation ensures that advisory-summary responses reflect the latest advisory correlations.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation logic after advisory-to-SBOM correlation step

## Implementation Notes
- Locate the advisory ingestion flow in `modules/ingestor/src/graph/advisory/mod.rs` (advisory ingestion: parse, store, correlate). After the step that links an advisory to an SBOM (the correlation step), add cache invalidation for the affected SBOM's advisory-summary cache key.
- The cache invalidation approach depends on the tower-http caching implementation used in the repository. If the cache supports key-based invalidation, invalidate the cache entry for `/api/v2/sbom/{id}/advisory-summary` where `{id}` is the SBOM being updated. If the cache is a simple TTL-based middleware without key-based invalidation, consider using a cache-busting mechanism (e.g., a version counter or timestamp in the cache layer).
- Reference `modules/ingestor/src/service/mod.rs` (IngestorService) for how the ingestion service is structured and how it interacts with other services.
- Per CONVENTIONS.md: use `.context()` wrapping for any error paths introduced by cache invalidation logic.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` module file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion flow where cache invalidation will be added
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module for reference on how ingestion modules are structured

## Acceptance Criteria
- [ ] After a new advisory is linked to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` return updated counts reflecting the newly linked advisory
- [ ] Cache invalidation does not introduce errors in the advisory ingestion pipeline

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, verify the summary endpoint returns updated counts without waiting for the 5-minute cache TTL
- [ ] Verify the advisory ingestion pipeline continues to function correctly after adding cache invalidation

## Dependencies
- Depends on: Task 3 — Add advisory-summary REST endpoint with caching
