## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint always returns up-to-date severity counts after new advisory data is ingested, as required by TC-9001.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after new advisory-to-SBOM links are created during ingestion

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. After the correlation step (where advisories are linked to SBOMs via the `sbom_advisory` join table in `entity/src/sbom_advisory.rs`), add a cache invalidation call for the affected SBOM's advisory-summary cache entry.
- Use the same `tower-http` caching mechanism configured in the endpoint (Task 2). If the cache uses a key-based invalidation pattern, invalidate the key corresponding to `/api/v2/sbom/{sbom_id}/advisory-summary`. If the cache is a global response cache, trigger a purge for the affected SBOM's summary route.
- Follow the existing ingestion pipeline patterns in `modules/ingestor/src/graph/sbom/mod.rs` and `modules/ingestor/src/graph/advisory/mod.rs` for how post-ingestion side effects are handled.
- Wrap any cache invalidation errors with `.context("Failed to invalidate advisory summary cache")` per the error handling convention. Cache invalidation failures should be logged but not fail the ingestion operation.
- Per CONVENTIONS.md §Error Handling: wrap errors with `.context()` and handle gracefully.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion and correlation logic; extend the correlation step with cache invalidation
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pipeline; reference for how post-ingestion side effects are structured

## Acceptance Criteria
- [ ] After a new advisory is linked to an SBOM during ingestion, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion reflect the updated advisory counts
- [ ] Cache invalidation failures are logged but do not fail the advisory ingestion operation
- [ ] Existing advisory ingestion behavior is preserved (no regressions)

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, then verify the advisory-summary endpoint returns updated counts (not stale cached data)
- [ ] Integration test: verify that advisory ingestion succeeds even if cache invalidation encounters an error (graceful degradation)

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
