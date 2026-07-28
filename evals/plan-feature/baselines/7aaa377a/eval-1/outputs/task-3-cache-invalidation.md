# Task 3 — Add cache invalidation for advisory severity summaries in ingestion pipeline

## Repository
trustify-backend

## Target Branch
main

## Description
Modify the advisory ingestion pipeline to invalidate cached advisory severity summaries when new advisories are linked to an SBOM. Without this, the `GET /api/v2/sbom/{id}/advisory-summary` endpoint could return stale counts for up to 5 minutes after new advisories are ingested. The cache invalidation should target the specific SBOM(s) affected by the newly ingested advisory.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation completes. When the ingestion pipeline links a new advisory to one or more SBOMs, invalidate the cached advisory-summary response for each affected SBOM ID.

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. Locate the correlation step where advisories are linked to SBOMs via the `sbom_advisory` join table.
- After the correlation step, extract the list of affected SBOM IDs and invalidate their cached `/advisory-summary` responses.
- The cache invalidation mechanism depends on the `tower-http` caching setup. If using an in-memory cache layer, invalidate by key (e.g., the SBOM-specific cache key). If using HTTP cache headers, consider setting `Cache-Control: no-cache` or a cache-busting mechanism on ingestion events.
- Reference the existing ingestion flow in `modules/ingestor/src/service/mod.rs` (`IngestorService`) to understand how the advisory ingestion graph is invoked.
- Per Key Conventions §Error handling: wrap cache invalidation errors with `.context()` and log warnings rather than failing the ingestion — cache staleness is preferable to ingestion failure.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion logic; extend with cache invalidation at the correlation step
- `entity/src/sbom_advisory.rs` — join table entity used during correlation; reference to identify affected SBOM IDs

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Cache invalidation targets only the affected SBOM IDs, not the entire cache
- [ ] Cache invalidation failures are logged as warnings but do not block advisory ingestion
- [ ] After ingestion of a new advisory, the next `GET /api/v2/sbom/{id}/advisory-summary` call returns updated counts

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, verify the advisory-summary endpoint returns updated counts without waiting for cache expiry
- [ ] Integration test: cache invalidation failure does not cause ingestion to fail

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
