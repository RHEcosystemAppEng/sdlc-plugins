## Repository
trustify-backend

## Target Branch
main

## Description
Hook into the advisory ingestion pipeline to invalidate cached advisory severity summaries when new advisories are linked to an SBOM. This ensures that the 5-minute in-memory cache for the GET /api/v2/sbom/{id}/advisory-summary endpoint does not serve stale data after new advisories are ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory ingestion completes and a new SBOM-advisory link is created

## Implementation Notes
The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles linking advisories to SBOMs. After the ingestion step that creates or updates entries in the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`), invoke the cache invalidation method to clear the cached summary for the affected SBOM ID(s). The cache structure is created in Task 3 (advisory summary endpoint) — this task connects the ingestion pipeline to the invalidation API. Use a shared cache reference (e.g., passed via application state or a dependency injection pattern consistent with how other shared state is managed in the ingestor module).
Per CONVENTIONS.md §Module pattern: modify the ingestor module following the project's module structure conventions. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module scope.

## Acceptance Criteria
- [ ] Ingesting a new advisory linked to an SBOM invalidates the cached summary for that SBOM
- [ ] Subsequent GET /api/v2/sbom/{id}/advisory-summary requests after ingestion reflect the new advisory counts
- [ ] Cache invalidation is targeted (only the affected SBOM's cache entry is cleared, not the entire cache)
- [ ] No performance regression in the ingestion pipeline

## Test Requirements
- [ ] Integration test verifying that cached summary is invalidated after a new advisory is ingested for an SBOM
- [ ] Integration test verifying that unrelated SBOM cache entries are not affected by ingestion for a different SBOM

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint
