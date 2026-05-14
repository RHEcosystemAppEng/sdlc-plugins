# Task 2 — Add cache invalidation for advisory severity summaries in the advisory ingestion pipeline

## Repository
trustify-backend

## Target Branch
main

## Description
When new advisories are ingested and linked to an SBOM, the cached advisory-summary response for that SBOM must be invalidated so that subsequent requests return up-to-date severity counts. Without this, the 5-minute cache introduced in Task 1 would serve stale data after new advisory correlations are processed. This task modifies the advisory ingestion pipeline to invalidate the relevant cache entries when SBOM-advisory links are created or updated.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation logic after the advisory correlation step (where advisories are linked to SBOMs via the `sbom_advisory` table). After successfully linking an advisory to one or more SBOMs, invalidate the cached advisory-summary for each affected SBOM ID.

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. The correlation step links advisories to SBOMs via the `sbom_advisory` entity. Cache invalidation should occur immediately after this correlation succeeds.
- Use the existing `tower-http` caching infrastructure for invalidation. The cache key for the advisory-summary endpoint is based on the request path `/api/v2/sbom/{id}/advisory-summary` — invalidate entries matching the SBOM IDs that were affected by the new advisory linkage.
- If the caching layer does not support targeted key invalidation (some `tower-http` cache implementations are opaque), an alternative approach is to store a per-SBOM cache version/timestamp in the database or an in-memory store, and have the endpoint check this version before serving cached responses. Inspect the existing cache configuration patterns in the endpoint route builders to determine the appropriate invalidation mechanism.
- Follow the existing error handling pattern in the ingestor module — cache invalidation failures should be logged as warnings but should not cause the ingestion to fail (fire-and-forget invalidation).
- Reference `modules/ingestor/src/service/mod.rs` for the `IngestorService` patterns and how the graph modules interact with the service layer.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory correlation logic where invalidation hooks should be added
- `modules/ingestor/src/service/mod.rs::IngestorService` — service layer pattern for the ingestor module

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` requests after advisory ingestion return updated counts reflecting the newly linked advisory
- [ ] Cache invalidation failures do not cause advisory ingestion to fail (logged as warnings)

## Test Requirements
- [ ] Integration test verifying that after ingesting a new advisory linked to an SBOM, the advisory-summary endpoint returns updated counts (not stale cached values)
- [ ] Test that cache invalidation failure does not block advisory ingestion

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model, service method, and REST endpoint
