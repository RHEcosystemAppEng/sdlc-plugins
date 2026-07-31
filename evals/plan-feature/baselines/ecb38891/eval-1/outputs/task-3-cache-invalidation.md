## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory severity summary for that SBOM is invalidated. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns fresh data after new advisory correlations are ingested, rather than serving stale cached counts.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation is established

## Implementation Notes
- The advisory ingestion module (`modules/ingestor/src/graph/advisory/mod.rs`) handles parsing, storing, and correlating advisories. After the correlation step that links an advisory to an SBOM (via the `sbom_advisory` join table), add a cache invalidation call for the affected SBOM's advisory summary.
- The cache invalidation mechanism depends on the tower-http cache configuration established in Task 2. If the cache uses an in-memory store with keyed entries, invalidate by SBOM ID. If the cache relies on HTTP cache-control headers (time-based expiry), the 5-minute TTL may be sufficient and this task may reduce to documenting the TTL-based invalidation strategy.
- Investigate how tower-http caching is currently configured in the existing endpoint route builders to determine the correct invalidation approach.
- Per repo Key Conventions §Module pattern: the ingestion logic follows the `graph/` module structure. The cache invalidation should be added at the correlation point in `graph/advisory/mod.rs`, not in a separate module.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` module file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — the existing advisory ingestion and correlation logic; the invalidation hook is added here
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for how SBOM ingestion handles post-processing steps

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM via the ingestion pipeline, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts reflecting the newly linked advisory
- [ ] Cache invalidation does not affect summaries for unrelated SBOMs

## Test Requirements
- [ ] Integration test verifying that after ingesting a new advisory linked to an SBOM, the advisory summary endpoint returns updated counts (not stale cached data)
- [ ] Test verifying that cache invalidation for one SBOM does not affect cached summaries for other SBOMs

## Verification Commands
- `cargo build --workspace` — project compiles without errors
- `cargo test -p ingestor` — ingestor module tests pass

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service
- Depends on: Task 2 — Add advisory summary endpoint with caching
