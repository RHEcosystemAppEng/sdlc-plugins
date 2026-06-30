# Task 4 — Add cache invalidation for advisory summary on advisory ingestion

## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory summary for that SBOM is invalidated. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns fresh data after new advisories are correlated with an SBOM, rather than serving stale cached counts.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation step to invalidate the advisory summary cache for affected SBOM IDs

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories — the cache invalidation should be triggered after the correlation step that links advisories to SBOMs
- Use the existing tower-http caching infrastructure referenced in the repository's Key Conventions (Caching) — the invalidation mechanism depends on how tower-http cache is configured (e.g., cache key eviction, cache-busting headers, or programmatic invalidation)
- Identify the cache key pattern used for the advisory summary endpoint (likely based on the SBOM ID path parameter) and invalidate entries matching affected SBOM IDs
- If tower-http does not support programmatic cache invalidation, consider alternative approaches: (a) use a shared cache store (e.g., an in-memory cache map) that the endpoint reads from and the ingestor can clear, or (b) use ETag/Last-Modified headers with a version counter that the ingestor increments
- Per the repository's Key Conventions (Error handling): any cache invalidation errors should be logged but not fail the ingestion pipeline — advisory ingestion must succeed even if cache invalidation fails.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` module file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — the advisory ingestion module where the invalidation hook will be added; inspect the correlation step to identify where SBOM IDs become known
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module; may show patterns for post-ingestion hooks or event publishing
- `modules/fundamental/src/sbom/endpoints/mod.rs` — the endpoint route registration where the cache is configured; shows the cache configuration pattern that the invalidation must match

## Acceptance Criteria
- [ ] When new advisories are linked to an SBOM during ingestion, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after advisory ingestion return updated counts
- [ ] Cache invalidation failures do not cause advisory ingestion to fail
- [ ] Cache invalidation only targets the affected SBOM IDs, not the entire cache

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, then verify that `GET /api/v2/sbom/{id}/advisory-summary` returns updated counts (not stale cached data)
- [ ] Integration test: verify that advisory ingestion succeeds even when cache invalidation encounters an error (if testable)

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching

<!-- [sdlc-workflow] Description digest: sha256-md:696b5506eea35f723e0e97f141c76f8d522706023a9af2150759914b5a58cdc3 -->
