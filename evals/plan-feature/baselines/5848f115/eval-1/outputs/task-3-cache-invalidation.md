## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation for the advisory-summary endpoint in the advisory ingestion pipeline. When new advisories are linked to an SBOM during ingestion, the cached advisory-summary response for that SBOM must be invalidated so that subsequent requests return fresh severity counts. This ensures the 5-minute cache (configured in Task 2) does not serve stale data after new advisory-SBOM correlations are ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation is persisted

## Implementation Notes
- The advisory ingestion module (`modules/ingestor/src/graph/advisory/mod.rs`) handles parsing, storing, and correlating advisories. After the correlation step that links an advisory to an SBOM (via the `sbom_advisory` join table), add a cache invalidation call for the affected SBOM's advisory-summary cache key.
- The invalidation mechanism should be consistent with how the `tower-http` caching middleware manages cache entries. Determine the cache key format used for the `/api/v2/sbom/{id}/advisory-summary` route and invalidate that specific key.
- If the caching infrastructure does not support programmatic invalidation of individual keys, consider using a cache-busting approach (e.g., a version counter or ETag stored alongside the SBOM-advisory relationship that the endpoint checks before returning cached data).
- Follow the existing error handling patterns in `modules/ingestor/src/graph/advisory/mod.rs` — wrap errors with `.context()`.
- Per Key Conventions: error handling — all code uses `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion and correlation logic; the invalidation call should be placed after the SBOM-advisory link creation
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — the endpoint handler (from Task 2) defines the cache configuration; reference its cache key format

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM during ingestion, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` calls after ingestion return updated severity counts
- [ ] Cache invalidation does not affect cached responses for unrelated SBOMs
- [ ] Ingestion pipeline continues to function correctly with the invalidation call (no performance regression)

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, verify the advisory-summary response reflects the new advisory immediately (not after cache expiry)
- [ ] Integration test: ingest an advisory for SBOM-A, verify SBOM-B's cached advisory-summary is not affected

## Verification Commands
- `cargo build -p ingestor` — compiles without errors
- `cargo test -p ingestor` — all existing and new tests pass

## Dependencies
- Depends on: Task 2 — Add advisory-summary endpoint with caching
