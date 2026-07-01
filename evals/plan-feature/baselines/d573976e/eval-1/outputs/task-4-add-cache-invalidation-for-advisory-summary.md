# Task 4 — Add cache invalidation for advisory-summary on advisory ingestion

## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory-summary for that SBOM is invalidated. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint always returns up-to-date severity counts after new advisory data is ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call when advisories are linked to SBOMs during ingestion

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories — this is where new advisory-to-SBOM links are created
- The existing caching infrastructure uses `tower-http` caching middleware — investigate the cache invalidation API available in the project's tower-http setup
- When the advisory ingestion pipeline creates or updates a link between an advisory and an SBOM (via the `sbom_advisory` join table defined in `entity/src/sbom_advisory.rs`), the cache entry for that SBOM's advisory-summary must be invalidated
- The invalidation should target the specific SBOM's cache key rather than clearing the entire cache — this preserves cached summaries for unaffected SBOMs
- Reference the SBOM ingestion module at `modules/ingestor/src/graph/sbom/mod.rs` for patterns on how the ingestor interacts with entities and cross-module concerns
- The `IngestorService` at `modules/ingestor/src/service/mod.rs` orchestrates the ingestion pipeline and may need to be extended if cache access requires service-level injection

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion pipeline where SBOM-advisory links are established
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module showing ingestor patterns for cross-entity operations
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity, the point where links are created

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` return updated counts reflecting the newly ingested advisory
- [ ] Cache invalidation targets only the affected SBOM(s), not the entire cache

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify that a subsequent advisory-summary request reflects the new advisory in its counts
- [ ] Test that cache invalidation is triggered during the advisory correlation step of ingestion

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
