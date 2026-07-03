# Task 3 — Add cache invalidation for advisory-summary on advisory ingestion

## Repository
trustify-backend

## Target Branch
main

## Description
Add a cache invalidation hook to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM. Without this, stale severity counts would be served for up to 5 minutes after new advisory data arrives, which could mislead dashboard users and alerting integrations.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation completes

## Implementation Notes
- The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories to SBOMs. After the correlation step (where advisory-SBOM links are created in the `sbom_advisory` table), add a call to invalidate the cached advisory-summary for the affected SBOM IDs.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module file scope.
- Use the existing tower-http cache infrastructure to invalidate specific cache entries. Identify the cache key pattern used by the advisory-summary endpoint (likely based on the request URL `/api/v2/sbom/{id}/advisory-summary`) and invalidate entries for all SBOM IDs that received new advisory links.
- If the caching layer does not support targeted key invalidation, consider using a cache-busting strategy (e.g., a version counter or timestamp stored alongside the cache, incremented on ingestion).
- Review how the SBOM ingestion pipeline (`modules/ingestor/src/graph/sbom/mod.rs`) handles similar post-ingestion side effects for patterns to follow.
- Per constraints doc section 5 (Code Change Rules): changes must be scoped to the files listed and must not duplicate existing cache invalidation logic.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pipeline for pattern reference on post-ingestion hooks
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion flow to extend
- `modules/ingestor/src/service/mod.rs::IngestorService` — service layer for the ingestor module

## Acceptance Criteria
- [ ] After advisory ingestion links a new advisory to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent GET /api/v2/sbom/{id}/advisory-summary requests after ingestion return updated counts (not stale cached data)
- [ ] Cache invalidation only affects the specific SBOM(s) that received new advisory links, not all cached summaries

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, verify advisory-summary returns updated counts
- [ ] Integration test: verify that advisory-summary for unrelated SBOMs remains cached (not invalidated)
- [ ] Integration test: verify cache invalidation works when multiple SBOMs are affected by a single advisory ingestion

## Verification Commands
- `cargo test --package ingestor -- advisory` — ingestion tests pass
- `cargo test --package fundamental -- advisory_summary` — endpoint tests still pass after invalidation changes

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute caching
