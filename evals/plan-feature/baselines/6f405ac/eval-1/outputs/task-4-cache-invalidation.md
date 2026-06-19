## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory-summary response for that SBOM is invalidated. This ensures the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns fresh data after advisory correlation completes.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — After the advisory-SBOM correlation step, add a call to invalidate the cached advisory-summary for the affected SBOM ID(s)

## Implementation Notes
The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. After the correlation step that links an advisory to an SBOM (inserting into the `sbom_advisory` join table via `entity/src/sbom_advisory.rs`), add a cache invalidation call.

Follow the existing `tower-http` caching patterns used in the codebase. The invalidation should target the cached response for `GET /api/v2/sbom/{id}/advisory-summary` for each SBOM ID that was linked to the newly ingested advisory.

Per CONVENTIONS.md §Caching: use `tower-http` caching middleware patterns for cache invalidation.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` Rust scope.

Per CONVENTIONS.md §Error handling: wrap invalidation errors with `.context()` — cache invalidation failures should log a warning but not fail the ingestion.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` Rust scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Existing advisory ingestion pipeline; extend the correlation step
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join entity; used to identify which SBOM IDs are affected

## Acceptance Criteria
- [ ] Advisory ingestion that links a new advisory to an SBOM triggers cache invalidation for that SBOM's advisory-summary
- [ ] Cache invalidation failure does not cause the advisory ingestion to fail (graceful degradation)
- [ ] After ingestion of a new advisory, subsequent `GET /api/v2/sbom/{id}/advisory-summary` returns updated counts

## Test Requirements
- [ ] Integration test verifying that after ingesting an advisory linked to an SBOM, the advisory-summary response reflects the new advisory
- [ ] Test verifying that cache invalidation failure is logged but does not block advisory ingestion

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (requires the cached endpoint to exist for invalidation to target)
