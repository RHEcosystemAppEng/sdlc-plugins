## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM. Without this, the `GET /api/v2/sbom/{id}/advisory-summary` endpoint would serve stale severity counts after new advisories are ingested, up to the 5-minute cache TTL. This fulfills the non-functional requirement from TC-9001: "advisory ingestion pipeline must invalidate cached summaries when new advisories are linked to an SBOM."

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation completes, targeting the advisory-summary cache entries for affected SBOMs

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. After the correlation step links an advisory to one or more SBOMs, insert a cache invalidation call for each affected SBOM's advisory-summary cache key.
- The cache key pattern must match the pattern used by the endpoint in Task 2 (e.g., keyed by SBOM ID for the `/api/v2/sbom/{id}/advisory-summary` route).
- Use the existing `tower-http` cache infrastructure — check how the cache layer is accessed from non-endpoint code. If the cache is not directly accessible from the ingestor module, consider using a shared cache handle or event-based invalidation pattern.
- Per CONVENTIONS.md §Error Handling: wrap cache invalidation errors with `.context()` and handle them gracefully — cache invalidation failure should log a warning but not fail the ingestion pipeline. See `modules/ingestor/src/graph/advisory/mod.rs` for the existing error handling pattern. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's .rs handler scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion pipeline showing the correlation step where cache invalidation should be inserted
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion for comparison, to check if similar cache invalidation patterns exist

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent GET /api/v2/sbom/{id}/advisory-summary calls after ingestion return updated counts without waiting for cache TTL expiry
- [ ] Cache invalidation failure does not cause the advisory ingestion to fail — errors are logged as warnings
- [ ] Cache invalidation targets only the affected SBOM's advisory-summary, not all cached responses

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, verify that the advisory-summary endpoint returns updated counts immediately
- [ ] Integration test: verify that cache invalidation failure is handled gracefully and does not block ingestion

## Dependencies
- Depends on: Task 2 — Add advisory-summary endpoint with caching (cache key pattern must be established first)
