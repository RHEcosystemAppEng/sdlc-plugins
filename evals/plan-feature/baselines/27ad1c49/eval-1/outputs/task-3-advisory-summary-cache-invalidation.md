## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM. When the ingestor correlates a new advisory with an SBOM, it must invalidate the cached summary for that SBOM to ensure the next request to `GET /api/v2/sbom/{id}/advisory-summary` returns fresh data.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — after linking an advisory to an SBOM in the correlation step, invalidate the advisory-summary cache entry for the affected SBOM ID

## Implementation Notes
Identify the point in the advisory ingestion flow where `sbom_advisory` records are inserted (the correlation step in `modules/ingestor/src/graph/advisory/mod.rs`). After each insert, collect the affected SBOM IDs and invalidate their cached advisory-summary responses. Use the same cache key pattern established by the endpoint's tower-http cache configuration in Task 2.

Per CONVENTIONS.md §Error handling: wrap cache invalidation errors with `.context()` and return `Result<T, AppError>` to avoid silent failures during ingestion.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust service scope.

Per CONVENTIONS.md §Caching: use the tower-http cache invalidation mechanism consistent with the cache configuration set up in the endpoint route builders.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's caching scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory correlation logic where cache invalidation calls should be inserted
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join entity used to identify affected SBOMs

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM during ingestion, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent GET /api/v2/sbom/{id}/advisory-summary requests after ingestion return updated counts
- [ ] Cache invalidation does not break the advisory ingestion pipeline on failure (errors are logged and wrapped, not silently swallowed)
- [ ] Multiple SBOMs affected by a single advisory ingestion each have their caches invalidated

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, verify that the advisory-summary endpoint returns updated counts
- [ ] Integration test: verify cache miss header after advisory ingestion for an affected SBOM

## Dependencies
- Depends on: Task 2 — Add advisory-summary endpoint with response caching
