# Task 4 -- Add cache invalidation for advisory-summary when advisories are ingested

## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new
advisories are linked to an SBOM, the cached advisory-summary for that SBOM is
invalidated. This ensures that `GET /api/v2/sbom/{id}/advisory-summary` returns
up-to-date counts after new advisory data is ingested, rather than serving stale
cached results for up to 5 minutes.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- add cache invalidation call after advisory-to-SBOM correlation completes

## Implementation Notes
- The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories to SBOMs. After the correlation step (where advisories are linked to SBOMs via the `sbom_advisory` join table), add a call to invalidate the cached advisory-summary for the affected SBOM(s).
- Determine the cache invalidation mechanism used by the existing tower-http caching middleware. The invalidation approach depends on how cache keys are structured:
  - If the cache is keyed by URL path, invalidate the cache entry for `/api/v2/sbom/{id}/advisory-summary` for each affected SBOM ID.
  - If the cache provides a programmatic eviction API, use it to clear the specific entries.
  - If the tower-http cache does not support selective invalidation, consider using an application-level cache (e.g., an in-memory TTL cache on the service layer) that can be explicitly cleared.
- Follow the error handling pattern used throughout the ingestor module -- cache invalidation failures should be logged but not block advisory ingestion (best-effort invalidation).
- Inspect the existing `IngestorService` in `modules/ingestor/src/service/mod.rs` to understand the service boundary and determine where the invalidation hook fits best architecturally.
- The SBOM ingestion pipeline (`modules/ingestor/src/graph/sbom/mod.rs`) may also need inspection to understand the full correlation flow, since advisory-SBOM links may be created during either SBOM or advisory ingestion.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` -- existing advisory ingestion and correlation logic; add invalidation after correlation
- `modules/ingestor/src/graph/sbom/mod.rs` -- SBOM ingestion logic; inspect for cross-references to advisory correlation

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts
- [ ] Cache invalidation failures are logged but do not block advisory ingestion
- [ ] Existing advisory ingestion behavior is not altered

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify that a subsequent call to the advisory-summary endpoint reflects the newly ingested advisory
- [ ] Integration test: verify that cache invalidation failure does not cause advisory ingestion to fail (simulate or force a cache error scenario)

## Dependencies
- Depends on: Task 2 -- Add GET /api/v2/sbom/{id}/advisory-summary endpoint
