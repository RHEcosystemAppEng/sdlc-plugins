## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are correlated with SBOMs, any cached advisory summary responses for the affected SBOMs are invalidated. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns fresh data after new advisories are ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — After the advisory ingestion process correlates an advisory with SBOMs (linking via `sbom_advisory`), add cache invalidation calls for the affected SBOM advisory-summary cache entries

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. After the correlation step (which inserts records into the `sbom_advisory` table), add logic to invalidate cached responses.
- The cache infrastructure uses `tower-http` caching middleware as noted in Key Conventions (Caching). Determine the invalidation mechanism by reviewing how the existing cache layer is configured — this may involve clearing cache entries keyed by the SBOM advisory-summary URL pattern, or using a shared cache store that supports key-based invalidation.
- Reference `modules/ingestor/src/graph/sbom/mod.rs` for the pattern of how the SBOM ingestion pipeline processes and links entities — the advisory ingestion follows a similar pattern.
- The invalidation should target only the specific SBOM IDs affected by the newly correlated advisory, not a global cache flush, to minimize performance impact.
- Per Key Conventions (Caching): uses `tower-http` caching middleware; cache configuration in endpoint route builders. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` file scope.
- Per Key Conventions (Error handling): all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` file scope.

## Acceptance Criteria
- [ ] Advisory ingestion pipeline invalidates cached advisory-summary responses for SBOMs affected by newly correlated advisories
- [ ] Invalidation targets only the specific SBOM IDs linked to the new advisory, not a global cache clear
- [ ] Existing advisory ingestion behavior (parse, store, correlate) is unchanged
- [ ] Cache invalidation errors are logged but do not fail the ingestion pipeline

## Test Requirements
- [ ] Integration test verifying that after ingesting a new advisory linked to an SBOM, the advisory-summary endpoint returns updated counts (not stale cached data)
- [ ] Test verifying that cache invalidation failure does not block advisory ingestion

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (cache invalidation depends on the cache being set up by the endpoint)


[sdlc-workflow] Description digest: sha256-md:37c9d3772ada872ca0e0869af127f069798cdb8657f8cb173cf08ca22bf4dc4b
