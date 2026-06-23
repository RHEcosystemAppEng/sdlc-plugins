## Repository
trustify-backend

## Target Branch
main

## Description
Update the advisory ingestion pipeline to invalidate cached advisory severity summaries when new advisories are linked to an SBOM. Without this, the cached summary endpoint could serve stale severity counts for up to 5 minutes after new advisories are correlated with an SBOM. The invalidation should target only the affected SBOM's cache entries, not flush all cached summaries globally.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — After the advisory-SBOM correlation step, emit a cache invalidation signal for the affected SBOM ID(s)
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — If a cache store or invalidation interface is needed in the handler, expose a method or handle to allow external invalidation

## Implementation Notes
The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. The correlation step links advisories to SBOMs via the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`). After this link is created, any cached advisory-summary response for the affected SBOM becomes stale.

Cache invalidation strategy depends on how the caching is implemented (from Task 4):
1. **If using in-memory cache (e.g., `moka` or a shared `HashMap`)** — inject the cache handle into the ingestor service and call `cache.invalidate(sbom_id)` after the correlation step.
2. **If using HTTP-level `Cache-Control` headers only** — there is no server-side cache to invalidate; the cache lives in downstream HTTP caches (CDN, browser). In this case, consider switching to a server-side cache in the handler that can be invalidated, or accept the staleness window as a known trade-off and document it.
3. **If using a cache abstraction/registry** — check `server/src/main.rs` and `common/` for an existing cache registry pattern.

The key insight: identify which SBOM IDs are affected during advisory ingestion. The ingestion code in `modules/ingestor/src/graph/advisory/mod.rs` already knows which SBOMs an advisory is being linked to — use those IDs for targeted invalidation.

If no existing cache invalidation pattern exists in the codebase, introduce a lightweight event or callback mechanism rather than tightly coupling the ingestor to the endpoint's cache. A simple approach: define a trait `CacheInvalidator` in `common/` and inject it into the ingestor.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion and SBOM correlation logic where invalidation must be triggered
- `entity/src/sbom_advisory.rs` — join table entity, used to determine which SBOMs are affected by an advisory ingestion
- `modules/ingestor/src/service/mod.rs::IngestorService` — service layer where cache invalidation handle can be injected

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM via ingestion, the cached severity summary for that SBOM is invalidated
- [ ] Invalidation is targeted — only the affected SBOM's cache entry is invalidated, not all cache entries
- [ ] Subsequent requests to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts
- [ ] Ingestion performance is not degraded by the invalidation step (no blocking I/O added to the hot path)

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify that the advisory-summary response reflects the new advisory (not stale cached data)
- [ ] Integration test: ingest an advisory for SBOM A, verify that SBOM B's cached summary is not invalidated (targeted invalidation)

## Dependencies
- Depends on: Task 4 — Advisory summary caching (needs the cache to be in place before invalidation can be implemented)

[sdlc-workflow] Description digest: sha256-md:d4cceb62aa9175e0dd5a32f0769cb472e52148e06e913b7a899a0ba0da46640e
