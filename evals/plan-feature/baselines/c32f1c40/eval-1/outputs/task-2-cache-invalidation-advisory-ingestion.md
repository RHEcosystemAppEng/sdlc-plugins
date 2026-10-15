## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM. Without this, the `GET /api/v2/sbom/{id}/advisory-summary` endpoint could serve stale severity counts for up to 5 minutes after new advisories are correlated.

This addresses the non-functional requirement: "Cache invalidation: advisory ingestion pipeline must invalidate cached summaries when new advisories are linked to an SBOM."

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after advisory-SBOM correlation step to invalidate cached advisory-summary for affected SBOM IDs

## Implementation Notes
The advisory ingestion module (`modules/ingestor/src/graph/advisory/mod.rs`) handles parsing, storing, and correlating advisories with SBOMs. After the correlation step that creates `sbom_advisory` records, add logic to invalidate the cached advisory-summary response for each affected SBOM.

Per CONVENTIONS.md: all handlers and service methods must return `Result<T, AppError>` with `.context()` wrapping for error propagation.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` module file scope.

**Cache invalidation approach:**
- Identify all SBOM IDs affected by the advisory ingestion (from the newly created `sbom_advisory` records)
- Invalidate the tower-http cache entries for those SBOM IDs' advisory-summary endpoints
- If tower-http does not support selective invalidation, consider using a cache key scheme that allows targeted invalidation, or switch to an application-level cache (e.g., `moka` or `cached` crate) for the advisory-summary endpoint
- Ensure cache invalidation failures do not block advisory ingestion (log and continue)

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Advisory ingestion module where the correlation step creates sbom_advisory records; the invalidation logic goes after this step
- `modules/ingestor/src/service/mod.rs::IngestorService` — Service orchestrating ingestion; may need to pass cache handle or invalidation callback

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent requests to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion reflect the updated advisory counts
- [ ] Cache invalidation failure does not prevent advisory ingestion from completing
- [ ] Existing advisory ingestion functionality is not broken

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, verify that the advisory-summary endpoint returns updated counts (not stale cached values)
- [ ] Integration test: verify advisory ingestion completes successfully even if cache invalidation encounters an error

## Verification Commands
- `cargo test --test api advisory` — Run advisory integration tests, expect all pass
- `cargo test --test api sbom` — Run SBOM integration tests including cache invalidation scenarios

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model, service, and endpoint
