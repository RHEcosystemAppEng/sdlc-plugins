## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory summary for that SBOM is invalidated. This ensures that `GET /api/v2/sbom/{id}/advisory-summary` returns fresh data after new advisory correlations are ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation is established

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. After the correlation step (where advisories are linked to SBOMs via the `sbom_advisory` join table), add a cache invalidation call for the affected SBOM's advisory summary.
- Investigate the existing tower-http caching middleware configuration to determine the cache invalidation mechanism. The caching middleware may support programmatic invalidation, or you may need to use a cache key pattern that allows targeted eviction.
- If the caching layer does not support targeted invalidation, consider alternative approaches:
  - Use an ETag/Last-Modified based caching strategy where the service layer checks a last-modified timestamp on the SBOM-advisory relationship
  - Add a `last_advisory_update` timestamp column to track when advisory correlations changed (but note the NFR: "no new database tables" — a column addition to an existing table may be acceptable)
- Follow the error handling pattern in `modules/ingestor/src/service/mod.rs` (IngestorService) for any new error paths.
- Per CONVENTIONS.md: caching uses tower-http caching middleware; cache configuration is in endpoint route builders. Coordinate the invalidation mechanism with the caching approach used in Task 2.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion logic; extend the correlation step with invalidation
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module; may show patterns for post-ingestion hooks or cache management

## Acceptance Criteria
- [ ] When a new advisory is correlated with an SBOM via the ingestion pipeline, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent GET requests to `/api/v2/sbom/{id}/advisory-summary` return updated counts after advisory ingestion
- [ ] No new database tables are introduced (per NFR)

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, verify that the advisory summary endpoint returns updated counts (not stale cached data)
- [ ] Integration test: verify that cache invalidation targets only the affected SBOM, not all cached summaries

## Dependencies
- Depends on: Task 2 — Add advisory summary endpoint with caching

---

> [sdlc-workflow] Description digest: (simulated) The digest would be posted as a Jira comment after task creation per the description-digest-protocol. Format: `[sdlc-workflow] Description digest: sha256-md:<64-hex-chars>`
