# Task 4: Add cache invalidation for advisory summaries on advisory ingestion

## Repository

trustify-backend

## Target Branch

main

## Description

When new advisories are linked to an SBOM during advisory ingestion, invalidate the cached advisory-summary response for the affected SBOM. This ensures that the 5-minute cache does not serve stale severity counts after new advisory data is ingested.

## Files to Modify

- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call when advisory-to-SBOM links are created or updated

## Implementation Notes

- Modify `modules/ingestor/src/graph/advisory/mod.rs` where advisory ingestion creates or updates `sbom_advisory` relationships.
- Identify the cache invalidation mechanism used by the existing tower-http caching middleware. This may involve:
  - Evicting a specific cache key based on the SBOM ID
  - Sending a cache-bust signal or event
  - Using a shared cache store that supports key-based invalidation
- The invalidation should target only the affected SBOM's advisory-summary cache entry, not the entire cache.
- Follow the existing patterns in the ingestion code for post-processing hooks or side effects after data is stored. See `modules/ingestor/src/graph/sbom/mod.rs` for a reference on how ingestion hooks are structured.
- If the caching layer does not support targeted key invalidation, consider using an application-level cache (e.g., a shared `HashMap<Uuid, (Instant, AdvisorySeveritySummary)>`) instead of relying solely on HTTP-level caching, and invalidate that.
- Per CONVENTIONS.md §Module pattern: the cache invalidation logic should be placed within the existing ingestion module structure, not in a new module.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module file scope.

## Reuse Candidates

- `entity/sbom_advisory.rs` — Understand the join table entity and when SBOM-advisory links are created
- `modules/ingestor/src/graph/advisory/mod.rs` — Existing advisory ingestion flow and post-processing patterns
- `modules/ingestor/src/graph/sbom/mod.rs` — Reference for ingestion hook patterns

## Acceptance Criteria

- [ ] When a new advisory is linked to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent requests to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return fresh data
- [ ] Only the affected SBOM's cache entry is invalidated, not the entire cache
- [ ] No new database tables are introduced (NFR)

## Test Requirements

- [ ] Integration test: ingest a new advisory linked to an SBOM, verify that the advisory-summary endpoint returns updated counts without waiting for cache expiry

## Dependencies

- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint (caching must be in place)

## Verification Commands

- `cargo check -p trustify-module-ingestor` — verify compilation
- `cargo test -p trustify-module-ingestor -- advisory` — run ingestion tests
