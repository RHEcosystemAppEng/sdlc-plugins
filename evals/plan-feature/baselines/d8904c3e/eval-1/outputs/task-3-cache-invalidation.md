## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory severity summaries are invalidated when new advisories are linked to an SBOM. Without this, the `GET /api/v2/sbom/{id}/advisory-summary` endpoint would serve stale severity counts for up to 5 minutes after new advisories are ingested. The invalidation must target only the affected SBOM's cached summary, not the entire cache.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation step

## Implementation Notes
- The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. After the correlation step (where an advisory is linked to an SBOM via the `sbom_advisory` join table), add a call to invalidate the cached advisory summary for the affected SBOM ID(s).
- Use the existing cache infrastructure referenced in the endpoint caching configuration. The invalidation mechanism depends on the tower-http cache implementation — if using an in-memory cache layer, invalidate by key; if using HTTP cache-control headers, consider adding a `must-revalidate` mechanism or an event-based invalidation pattern.
- Follow the error handling pattern established in `modules/ingestor/src/graph/advisory/mod.rs` — wrap any cache invalidation errors with `.context("cache invalidation for advisory summary")` and log warnings rather than failing the ingestion pipeline.
- Reference the `IngestorService` in `modules/ingestor/src/service/mod.rs` for the service architecture that the ingestion pipeline follows.
- Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for cache invalidation errors.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion logic where the invalidation hook needs to be added
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for ingestion pipeline patterns in a sibling module
- `modules/ingestor/src/service/mod.rs::IngestorService` — service layer that orchestrates ingestion

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM during ingestion, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` calls after ingestion return updated counts
- [ ] Cache invalidation failure does not block or fail the advisory ingestion pipeline (graceful degradation)

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, verify that the advisory-summary endpoint returns updated counts without waiting for cache expiry
- [ ] Test: cache invalidation error is logged as a warning but does not prevent advisory ingestion from completing

## Verification Commands
- `cargo build -p ingestor` — compiles without errors
- `cargo test -p ingestor -- advisory` — all ingestion tests pass

## Dependencies
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
