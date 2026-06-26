# Task 4 — Cache Invalidation on Advisory Ingestion

## Repository
trustify-backend

## Target Branch
main

## Description
Update the advisory ingestion pipeline to invalidate cached advisory summary responses when new advisories are linked to an SBOM. Without this, the `GET /api/v2/sbom/{id}/advisory-summary` endpoint would serve stale counts for up to 5 minutes after new advisories are correlated with an SBOM. The invalidation must cover all code paths in the advisory ingestion module that create or update SBOM-advisory relationships.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — After the code that inserts rows into the `sbom_advisory` join table (correlating advisories with SBOMs), add cache invalidation logic. Identify the affected SBOM IDs from the newly created `sbom_advisory` records and invalidate or purge their cached advisory summary responses.

## Implementation Notes
Examine the existing advisory ingestion flow in `modules/ingestor/src/graph/advisory/mod.rs` to find where `sbom_advisory` records are inserted. The cache invalidation should happen after a successful insert/commit, not before.

The invalidation approach depends on how the `tower-http` cache is structured in the codebase:
1. If using an in-process cache (e.g., `tower-http`'s `CacheLayer` with a shared cache store), invalidate by removing entries keyed on the SBOM ID path.
2. If using HTTP `Cache-Control` headers only (browser/CDN caching), server-side invalidation may not be possible — in that case, consider switching to an application-level cache (e.g., a `DashMap` or `moka` cache) for the advisory summary endpoint and invalidating entries there.

The ingestor module (`modules/ingestor/`) is a separate crate from `modules/fundamental/`, so the invalidation interface must be accessible across crate boundaries. Consider adding a cache invalidation trait or a shared cache handle that the ingestor can call.

Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` structure for any new files. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` module file scope.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` file scope.

## Acceptance Criteria
- [ ] Advisory ingestion that links new advisories to an SBOM triggers cache invalidation for that SBOM's advisory summary
- [ ] Cache invalidation covers all code paths that insert into the `sbom_advisory` table
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` calls return updated counts after ingestion completes
- [ ] Cache invalidation does not break existing advisory ingestion behavior
- [ ] `cargo check` passes with no errors

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify cached summary is updated on next request
- [ ] Test that advisory ingestion without SBOM linkage does not trigger unnecessary invalidation

## Dependencies
- Depends on: Task 3 — Advisory Summary Endpoint and Route Registration (endpoint must exist and be cached before invalidation is meaningful)

[sdlc-workflow] Description digest: sha256-md:7c02b03fec0f24f681fdb13151ec568f4533ac6483d6e53078a010707803d7f4
