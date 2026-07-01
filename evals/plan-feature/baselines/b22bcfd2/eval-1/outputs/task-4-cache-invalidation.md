## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory-summary for that SBOM is invalidated. This ensures the severity aggregation endpoint returns fresh data after advisory correlation updates, meeting the non-functional requirement that advisory ingestion must invalidate cached summaries.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call when advisories are correlated with SBOMs

## Implementation Notes
In `modules/ingestor/src/graph/advisory/mod.rs`, the advisory ingestion process parses, stores, and correlates advisories with SBOMs. After the correlation step (where `sbom_advisory` join records are inserted), add a cache invalidation call for the advisory-summary cache of affected SBOMs.

The invalidation approach depends on how `tower-http` caching is configured in the project:
1. If using an in-memory cache layer, invalidate the cache key corresponding to `/api/v2/sbom/{id}/advisory-summary` for each SBOM ID that was linked to the new advisory
2. If using HTTP cache-control headers only (client-side caching), no server-side invalidation is needed — the 5-minute TTL handles staleness

Follow the existing patterns in `modules/ingestor/src/graph/advisory/mod.rs` for post-ingestion hooks. The SBOM IDs affected by the advisory correlation can be extracted from the `sbom_advisory` records created during ingestion.

Reference `modules/ingestor/src/graph/sbom/mod.rs` for the SBOM ingestion pattern (parse, store, link) as a structural parallel.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion and correlation logic
- `modules/ingestor/src/service/mod.rs::IngestorService` — service layer for ingestion operations

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts
- [ ] Cache invalidation does not break existing advisory ingestion flow
- [ ] No performance regression in advisory ingestion pipeline

## Test Requirements
- [ ] Integration test: ingest advisory, verify summary, ingest new advisory for same SBOM, verify summary updates
- [ ] Test that cache invalidation targets only the affected SBOM IDs, not all cached summaries

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching

## additional_fields
- priority: Major
- fixVersions: RHTPA 1.5.0