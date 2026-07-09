## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory severity summaries are invalidated when new advisories are linked to an SBOM. Currently, the ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` parses, stores, and correlates advisories. After correlation (linking an advisory to an SBOM), the cached summary for the affected SBOM must be invalidated to ensure the next `GET /api/v2/sbom/{id}/advisory-summary` call returns fresh data.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation completes

## Implementation Notes
- The advisory ingestion module (`modules/ingestor/src/graph/advisory/mod.rs`) handles parsing, storing, and correlating advisories with SBOMs. Locate the correlation step where `sbom_advisory` join records are created.
- After creating `sbom_advisory` records, invalidate the cache entry for the affected SBOM's advisory-summary endpoint. The specific invalidation mechanism depends on how tower-http caching is configured — it may use cache keys based on the request path, or a shared cache store that supports explicit invalidation.
- If tower-http's cache does not support explicit key invalidation, consider using a separate application-level cache (e.g., an in-memory HashMap with TTL) for the advisory-summary endpoint that can be explicitly cleared.
- Per CONVENTIONS.md §Error Handling: wrap any cache invalidation errors with `.context()` to provide meaningful error messages without failing the ingestion pipeline.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion logic; add invalidation alongside the correlation step
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pattern for reference on post-ingestion hooks

## Acceptance Criteria
- [ ] Cached advisory-summary response is invalidated when new advisories are linked to an SBOM
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` call after ingestion returns updated counts
- [ ] Cache invalidation failure does not block the advisory ingestion pipeline (best-effort invalidation)

## Test Requirements
- [ ] Integration test: advisory-summary response updates after a new advisory is ingested and linked to the SBOM
- [ ] Integration test: ingestion succeeds even if cache invalidation encounters an error

## Dependencies
- Depends on: Task 2 — Add advisory-summary endpoint with caching
