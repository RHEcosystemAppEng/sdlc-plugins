## Repository
trustify-backend

## Target Branch
main

## Description
Update the advisory ingestion pipeline to invalidate cached advisory summaries when new advisories are linked to an SBOM. When the ingestor correlates a new advisory with an SBOM, the cached response for `GET /api/v2/sbom/{id}/advisory-summary` must be invalidated so that subsequent requests return fresh severity counts.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation logic after advisory-SBOM correlation step, targeting the advisory summary cache entries for affected SBOMs

## Implementation Notes
The advisory ingestion flow in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. After the correlation step that links an advisory to an SBOM (via the `sbom_advisory` join table from `entity/src/sbom_advisory.rs`), add a cache invalidation call.

Use the existing cache infrastructure referenced by the tower-http caching middleware. The invalidation should target the specific SBOM's advisory summary cache key. If the cache layer uses URL-based keys, invalidate the key for `/api/v2/sbom/{id}/advisory-summary` where `{id}` is the affected SBOM ID.

Look at how `IngestorService` (`modules/ingestor/src/service/mod.rs`) orchestrates ingestion to understand where the correlation step occurs and where to insert the invalidation hook.

Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for error paths in the invalidation logic.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module, demonstrates the pattern for post-ingestion hooks
- `modules/ingestor/src/service/mod.rs::IngestorService` — orchestration entry point for ingestion flow

## Acceptance Criteria
- [ ] Advisory ingestion invalidates the advisory summary cache for affected SBOMs
- [ ] Cache invalidation occurs after advisory-SBOM correlation completes
- [ ] Subsequent GET requests to `/api/v2/sbom/{id}/advisory-summary` return updated counts after new advisory ingestion
- [ ] Existing advisory ingestion functionality is not broken

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, verify the advisory summary reflects the new advisory after cache invalidation
- [ ] Verify advisory ingestion still completes successfully with the invalidation logic added

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (cache must exist before invalidation can target it)
