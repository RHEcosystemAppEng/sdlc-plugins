## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic in the advisory ingestion pipeline so that cached advisory summary responses are invalidated when new advisories are linked to an SBOM. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns fresh data after advisory ingestion completes.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation hook after advisory-SBOM correlation completes

## Implementation Notes
- Reference the existing advisory ingestion flow in `modules/ingestor/src/graph/advisory/mod.rs` to understand where advisory-SBOM links are created
- Reference `modules/ingestor/src/graph/sbom/mod.rs` for SBOM ingestion patterns and any existing cache invalidation examples
- Reference `modules/ingestor/src/service/mod.rs` for `IngestorService` to understand the service layer
- The invalidation should occur after the advisory is correlated with SBOMs (after `sbom_advisory` records are inserted/updated)
- Use the same caching mechanism configured on the endpoint in Task 3 — invalidate the cache entry keyed by the affected SBOM IDs
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module scope.

## Acceptance Criteria
- [ ] Cache invalidation fires after new advisory-SBOM correlations are stored
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` calls return updated counts after ingestion
- [ ] Cache invalidation does not break existing advisory ingestion flow

## Test Requirements
- [ ] Test that ingesting a new advisory updates cached summary counts
- [ ] Test that ingestion without new SBOM links does not trigger unnecessary invalidation
- [ ] Test that existing advisory ingestion tests still pass

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint with caching
