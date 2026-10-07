## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation for advisory severity summaries during advisory ingestion (TC-9001). When the advisory ingestion pipeline links new advisories to an SBOM, the cached advisory-summary response for that SBOM must be invalidated so subsequent requests return up-to-date severity counts. This ensures data consistency between the ingestion pipeline and the aggregation endpoint.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation completes, targeting the cached advisory-summary responses for affected SBOM IDs

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. After the correlation step (where advisories are linked to SBOMs via the `sbom_advisory` join table), insert a cache invalidation call.
- Use the tower-http cache invalidation mechanism (or the cache store's eviction API) to remove cached responses for the affected SBOM's advisory-summary endpoint. The cache key is derived from the request path `/api/v2/sbom/{id}/advisory-summary`.
- Reference the SBOM ingestion module at `modules/ingestor/src/graph/sbom/mod.rs` for how ingestion pipelines are structured and how to access shared services.
- Per CONVENTIONS.md §Caching: follow the established tower-http caching patterns for invalidation. See `modules/fundamental/src/sbom/endpoints/mod.rs` for how caching is configured, which informs how to target cache entries for invalidation. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion logic; the invalidation hook is added at the end of the correlation step within this module
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module; reference for ingestion pipeline structure and service access patterns

## Acceptance Criteria
- [ ] After advisory ingestion links a new advisory to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` requests after ingestion return updated severity counts
- [ ] Cache invalidation does not affect advisory-summary caches for unrelated SBOMs

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify the advisory-summary endpoint returns updated counts after ingestion
- [ ] Integration test: verify that advisory-summary caches for other SBOMs are not invalidated during ingestion

## Verification Commands
- `cargo build` — project compiles without errors
- `cargo test` — all existing tests continue to pass

## Dependencies
- Depends on: Task 2 — Add advisory-summary endpoint with caching
