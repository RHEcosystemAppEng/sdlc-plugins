## Repository
trustify-backend

## Target Branch
main

## Description
Modify the advisory ingestion pipeline to invalidate the cached advisory-summary response when new advisories are linked to an SBOM. This ensures that stale cached severity counts are evicted when the advisory ingestion pipeline creates new advisory-SBOM correlations in the `sbom_advisory` table, keeping the summary endpoint accurate without waiting for the 5-minute cache TTL to expire.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation is created in the ingestion pipeline

## Implementation Notes
- Locate the section in `modules/ingestor/src/graph/advisory/mod.rs` where new `sbom_advisory` records are inserted (the advisory correlation step). After each successful correlation, trigger cache invalidation for the affected SBOM's advisory-summary endpoint.
- Use the tower-http cache purge mechanism or key-based invalidation to target specifically the cached response for `GET /api/v2/sbom/{affected_sbom_id}/advisory-summary`. Do not purge unrelated cached responses.
- Reference the SBOM ingestion pipeline in `modules/ingestor/src/graph/sbom/mod.rs` for patterns on how post-processing hooks are structured after data insertion.
- Cache invalidation failures must be handled gracefully: log the error with `.context()` wrapping but do not propagate the failure to the caller. Advisory ingestion must succeed even if cache invalidation fails.
- If the ingestion pipeline links an advisory to multiple SBOMs in a batch, invalidate the cache for each affected SBOM.

Per CONVENTIONS.md §Error Handling: wrap cache invalidation errors with `.context()` and log them, but do not propagate failures to the ingestion caller — ingestion must not fail due to cache invalidation.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory correlation logic where the invalidation hook should be added
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for how the SBOM ingestion pipeline handles post-insertion processing steps

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached advisory-summary response for that SBOM is invalidated
- [ ] Cache invalidation targets only the affected SBOM's advisory-summary, not the entire cache
- [ ] Advisory ingestion completes successfully even if cache invalidation fails (graceful degradation)
- [ ] When an advisory is linked to multiple SBOMs in a single ingestion, all affected caches are invalidated

## Test Requirements
- [ ] Integration test: after ingesting a new advisory linked to an SBOM, a subsequent GET to advisory-summary returns updated counts (not stale cached data)
- [ ] Test: cache invalidation failure does not cause advisory ingestion to fail

## Dependencies
- Depends on: Task 2 — Create GET /api/v2/sbom/{id}/advisory-summary endpoint with caching

---

[sdlc-workflow] Description digest: sha256-md:37e9bcee56bf88e177e56989d78f985c79fc1ca91a944470f3bdf5e87cf37384
