## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory severity summaries are invalidated when new advisories are linked to an SBOM. When the ingestor correlates a new advisory with an SBOM (via the sbom_advisory join table), the cached response for that SBOM's advisory-summary endpoint must be evicted. This ensures consumers always see up-to-date severity counts after new advisory data is ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation is persisted; when a new row is inserted into sbom_advisory, invalidate the cached advisory-summary for the affected SBOM ID(s)
- `modules/ingestor/Cargo.toml` — add dependency on the cache infrastructure if not already present

## Implementation Notes
- The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` parses, stores, and correlates advisories with SBOMs. Locate the point where `sbom_advisory` rows are inserted (the correlation step) and add cache invalidation after successful insertion.
- Follow the tower-http caching infrastructure already used in endpoint route builders. Determine whether the project uses a shared cache store (e.g., an in-memory cache or external cache like Redis) that can be explicitly invalidated, or whether cache invalidation requires a different mechanism (e.g., cache key versioning, ETag-based invalidation).
- If the cache infrastructure does not support explicit eviction, consider implementing a cache version counter per SBOM ID that is incremented on advisory ingestion — the endpoint would include the version in its cache key, causing a cache miss after ingestion.
- The `IngestorService` in `modules/ingestor/src/service/mod.rs` may need to accept a reference to the cache store or invalidation mechanism via dependency injection, following existing patterns for how services receive dependencies.
- Per docs/constraints.md section 5 (Code Change Rules): changes scoped to listed files, inspect code before modifying, follow referenced patterns, do not duplicate existing functionality.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — the advisory ingestion module where correlation logic lives; inspect this to find the exact insertion point for cache invalidation
- `modules/ingestor/src/service/mod.rs::IngestorService` — the service that orchestrates ingestion; may need to pass cache references through this layer

## Acceptance Criteria
- [ ] When a new advisory is correlated with an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent calls to GET /api/v2/sbom/{id}/advisory-summary after ingestion return fresh (non-cached) data
- [ ] Cache invalidation does not impact the performance of the ingestion pipeline (invalidation should be a lightweight operation)
- [ ] No existing ingestion behavior is broken by the change

## Test Requirements
- [ ] Integration test verifying that after advisory ingestion for an SBOM, the advisory-summary endpoint returns updated counts (covered in Task 4)
- [ ] Verify that the ingestion pipeline still completes successfully after the change

## Verification Commands
- `cargo build -p ingestor` — verify the ingestor module compiles without errors
- `cargo test -p ingestor` — verify existing ingestor tests still pass

## Dependencies
- Depends on: Task 2 — Add advisory summary endpoint (the cache to invalidate is set up in the endpoint)
