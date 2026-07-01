## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM. This ensures that the 5-minute cache on the advisory-summary endpoint does not serve stale data after new advisory correlations are ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation is stored

## Implementation Notes
- The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. After the step that links an advisory to SBOMs (via the `sbom_advisory` join table), add a cache invalidation call for the affected SBOM IDs.
- Inspect the existing caching middleware configuration to determine the invalidation mechanism. If tower-http cache is configured with a shared cache store, invalidate entries by cache key (likely the endpoint path `/api/v2/sbom/{id}/advisory-summary`). If no programmatic invalidation API exists, consider using cache-control headers with `must-revalidate` and tracking a version/ETag in the service layer.
- Do not introduce new database tables — use existing infrastructure per the non-functional requirements.
- Per CONVENTIONS.md §Module pattern: keep the invalidation logic in the ingestor module where the correlation happens. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module file scope.
- Per CONVENTIONS.md §Error handling: wrap any cache invalidation errors with `.context()` and handle gracefully (log but do not fail the ingestion). Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion logic to extend
- `modules/ingestor/src/graph/sbom/mod.rs` — sibling ingestion module for reference on post-ingestion hooks

## Acceptance Criteria
- [ ] After advisory ingestion links a new advisory to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Advisory ingestion does not fail if cache invalidation encounters an error (graceful degradation)
- [ ] No new database tables are introduced

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM and verify the advisory-summary endpoint returns updated counts (not stale cached data)
- [ ] Integration test: cache invalidation errors do not cause advisory ingestion to fail

## Verification Commands
- `cargo check -p trustify-module-ingestor` — compiles without errors
- `cargo test -p trustify-module-ingestor` — ingestor tests pass

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint

[sdlc-workflow] Description digest: sha256-md:9ef4ebed80f1577112915f6e110cd70e4d1c761be7262e128e175367029041eb
