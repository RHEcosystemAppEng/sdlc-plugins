## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM (TC-9001). When the ingestor correlates a new advisory with an SBOM, it must invalidate or evict the cached response for that SBOM's `advisory-summary` endpoint to ensure consumers see up-to-date severity counts.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation

## Implementation Notes
- Identify the point in the advisory ingestion flow (within `modules/ingestor/src/graph/advisory/mod.rs`) where an advisory is linked to an SBOM via the `sbom_advisory` join table. After this link is created, trigger cache invalidation for the affected SBOM's advisory-summary cache entry.
- Use the existing `tower-http` caching infrastructure for invalidation. If the cache is key-based (e.g., keyed by request path), invalidate the entry for `/api/v2/sbom/{sbom_id}/advisory-summary`. If the cache uses a shared state or TTL-based eviction only, document the approach and any limitations.
- If no programmatic cache invalidation API exists in the current caching setup (i.e., `tower-http` caching is purely TTL-based with no manual eviction), implement an application-level cache (e.g., a shared `HashMap` with TTL or a `moka` cache) that the endpoint reads and the ingestor invalidates. Document this decision in a code comment.
- Per CONVENTIONS.md §Error Handling: use `.context()` wrapping on any fallible cache invalidation operations. Cache invalidation failures should be logged but not block advisory ingestion.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion and correlation logic; extend this module with the invalidation call
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module; reference for understanding how SBOM IDs are propagated during ingestion

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM during ingestion, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after invalidation return updated severity counts
- [ ] Cache invalidation failures are logged but do not block the advisory ingestion pipeline

## Test Requirements
- [ ] Test that ingesting a new advisory for an SBOM causes the advisory-summary cache to be invalidated (the next request returns fresh data)
- [ ] Test that cache invalidation failure does not prevent advisory ingestion from completing

## Dependencies
- Depends on: Task 1 — Add advisory severity count model and service method
