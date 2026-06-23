## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory severity summary for that SBOM is invalidated. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns fresh data after advisory correlation updates.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation to invalidate the advisory summary cache for affected SBOM IDs

## Implementation Notes
- Inspect `modules/ingestor/src/graph/advisory/mod.rs` to understand the advisory ingestion flow, specifically the point where advisories are correlated (linked) to SBOMs via the `sbom_advisory` join table.
- After the correlation step, extract the SBOM IDs that were affected and invalidate the cache entries for those SBOMs.
- The invalidation mechanism depends on how the `tower-http` caching is implemented in this repository:
  - If using in-memory cache with `tower-http`: invalidate by key (SBOM ID) or clear the relevant cache layer.
  - If using HTTP `Cache-Control` headers only: consider adding a cache-buster mechanism (e.g., ETag or Last-Modified based on the latest advisory correlation timestamp).
- Inspect `modules/ingestor/src/graph/sbom/mod.rs` for reference on how the SBOM ingestion pipeline handles similar post-processing steps.
- Also inspect `modules/ingestor/src/service/mod.rs` (`IngestorService`) for any existing cache invalidation patterns.
- Per docs/constraints.md §5.2: inspect the ingestion code before modifying it.
- Per docs/constraints.md §5.4: reuse any existing cache invalidation utilities rather than duplicating logic.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion pipeline where invalidation must be added
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for post-ingestion processing patterns
- `modules/ingestor/src/service/mod.rs::IngestorService` — check for existing cache invalidation patterns

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the advisory summary cache for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts
- [ ] Cache invalidation only affects the specific SBOM(s) linked to the newly ingested advisory, not all cached summaries
- [ ] Project compiles successfully with `cargo check`

## Test Requirements
- [ ] Integration test verifying that after ingesting a new advisory linked to an SBOM, the advisory summary endpoint returns updated severity counts (not stale cached data)
- [ ] Test verifying that cache entries for unrelated SBOMs are not invalidated

## Dependencies
- Depends on: Task 4 — Advisory summary caching

[sdlc-workflow] Description digest: sha256-md:19f78d12603007a9ab447915e3fac645b00c530d36b0d4c096273eb164ed692c
