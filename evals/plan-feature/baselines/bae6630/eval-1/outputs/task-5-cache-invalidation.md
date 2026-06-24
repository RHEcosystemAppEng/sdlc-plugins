## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory severity summary for that SBOM is invalidated. This ensures the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns fresh data after new advisory correlations are ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after advisory-SBOM correlation is completed

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs`, the advisory ingestion logic parses advisories, stores them, and correlates them with SBOMs. After the correlation step (where entries are inserted into the `sbom_advisory` join table), add a cache invalidation call.
- The existing cache infrastructure uses `tower-http` caching middleware. Determine the cache invalidation mechanism: this may involve clearing a cache key derived from the SBOM ID, or sending an invalidation signal if the cache layer supports it.
- If the caching is purely HTTP-level (via `Cache-Control` headers and a reverse proxy), invalidation may not be possible server-side. In that case, consider switching to an application-level cache (e.g., an in-memory `HashMap` with TTL) that can be explicitly invalidated, or document that cache invalidation relies on TTL expiry.
- Follow the error handling pattern in `modules/ingestor/src/graph/advisory/mod.rs` — use `.context()` wrapping on any fallible cache operations.
- Reference the `IngestorService` in `modules/ingestor/src/service/mod.rs` for how services are structured in the ingestor module.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Existing advisory ingestion and correlation logic; the invalidation call is added at the end of the correlation step
- `modules/ingestor/src/service/mod.rs::IngestorService` — Service patterns in the ingestor module
- `entity/src/sbom_advisory.rs` — Join table entity; the correlation step inserts rows here, identifying which SBOM IDs need cache invalidation

## Acceptance Criteria
- [ ] When a new advisory is correlated with an SBOM, the cached advisory summary for that SBOM is invalidated
- [ ] Cache invalidation does not cause errors in the ingestion pipeline (failures are logged but do not block ingestion)
- [ ] The invalidation targets only the affected SBOM's cached summary, not all cached data

## Test Requirements
- [ ] After ingesting a new advisory linked to an SBOM, a subsequent call to the summary endpoint returns updated counts (not stale cached data)
- [ ] Cache invalidation failure does not cause the ingestion to fail

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (caching must be implemented before invalidation can target it)

## Digest
[sdlc-workflow] Description digest: sha256-md:824d0248e1305637030e6721110ab5575b2c61ab743f248ce8cb70dd30e5a63b
