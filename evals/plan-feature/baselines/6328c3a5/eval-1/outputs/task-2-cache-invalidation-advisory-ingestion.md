## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation for advisory severity summary responses in the advisory ingestion pipeline. When new advisories are linked to an SBOM during ingestion, the cached severity summary for that SBOM must be invalidated so that subsequent requests to `GET /api/v2/sbom/{id}/advisory-summary` return up-to-date counts.

This is a non-functional requirement from the feature specification: the advisory ingestion pipeline must invalidate cached summaries when new advisories are linked to an SBOM.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation logic after advisory-SBOM correlation completes, targeting the cached response for the advisory-summary endpoint

## Implementation Notes
- Per CONVENTIONS.md §Error Handling: use `.context()` wrapping for any errors during cache invalidation. See `modules/fundamental/src/sbom/endpoints/get.rs` for the error handling pattern.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` handler scope.
- Per CONVENTIONS.md §Framework: use the existing tower-http cache infrastructure to invalidate entries.
  Applies: convention has no file-type restriction (broadly applicable).
- The cache invalidation must target all SBOM IDs that were affected by the newly ingested advisory. After the advisory-SBOM correlation step in the ingestion pipeline, collect the set of affected SBOM IDs and invalidate their cached summary responses.
- If the cache infrastructure supports key-based invalidation, invalidate by the endpoint cache key for each affected SBOM. If it only supports time-based expiry, document this limitation and rely on the 5-minute TTL.
- Ensure cache invalidation does not introduce significant latency into the ingestion pipeline — it should be a lightweight operation.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion flow showing where the correlation step occurs and how post-correlation operations are structured
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion flow for reference on how the ingestion pipeline handles post-ingestion operations

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached severity summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts reflecting the new advisory
- [ ] Cache invalidation does not affect unrelated SBOM summary caches (only affected SBOMs are invalidated)
- [ ] No measurable performance degradation in the advisory ingestion pipeline due to cache invalidation

## Test Requirements
- [ ] Test that ingesting a new advisory linked to an SBOM causes the summary cache to be invalidated
- [ ] Test that the severity summary reflects the new advisory after cache invalidation
- [ ] Test that SBOMs not linked to the new advisory retain their cached summaries

## Verification Commands
- `cargo test --package tests -- advisory` — run advisory-related integration tests

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation endpoint (the cache must exist before it can be invalidated)
