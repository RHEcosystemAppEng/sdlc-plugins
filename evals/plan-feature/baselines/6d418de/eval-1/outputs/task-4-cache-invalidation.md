# Task 4 — Add cache invalidation for advisory summary on advisory ingestion

## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory summary for that SBOM is invalidated. This ensures the `GET /api/v2/sbom/{id}/advisory-summary` endpoint always returns up-to-date severity counts after new advisory data is ingested. Without this, stale cached summaries could persist for up to 5 minutes after new advisories are correlated.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation completes

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. The cache invalidation hook should be added at the point where the advisory-SBOM linkage is persisted (after the `sbom_advisory` join table is updated).
- Use the existing `tower-http` caching infrastructure. The invalidation mechanism depends on how the project configures its cache — typical approaches include:
  - Purging cache entries by key/path pattern (e.g., invalidate entries matching `/api/v2/sbom/{affected-sbom-id}/advisory-summary`)
  - Setting a shared cache store that the endpoint and ingestor both reference
- Inspect the existing caching setup in the endpoint route builders to understand how cache entries are keyed and how to invalidate them programmatically.
- This is a non-functional requirement: advisory ingestion pipeline must invalidate cached summaries when new advisories are linked to an SBOM.
- Per docs/constraints.md Section 5 (Code Change Rules): changes must be scoped to the files listed; code must not be modified without first inspecting it; implementation must follow the patterns referenced in these notes.
- Per docs/constraints.md Section 2 (Commit Rules): every commit must reference TC-9001, follow Conventional Commits, and include the AI assistance trailer.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — the advisory ingestion module where the correlation logic lives; inspect to find the exact insertion point for the invalidation hook
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module; may demonstrate existing cache invalidation patterns if any exist in the ingestor

## Acceptance Criteria
- [ ] Advisory ingestion pipeline invalidates the cached advisory summary for affected SBOMs when new advisories are linked
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` calls after ingestion return updated counts without waiting for cache expiry
- [ ] Existing advisory ingestion behavior is not altered beyond the cache invalidation addition

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, then verify that `GET /api/v2/sbom/{id}/advisory-summary` returns updated counts reflecting the newly ingested advisory
- [ ] Integration test: verify that advisory ingestion for an SBOM that has no cached summary does not cause errors (no-op invalidation)

## Verification Commands
- `cargo build` — full project compiles
- `cargo test --test api` — integration tests pass

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
