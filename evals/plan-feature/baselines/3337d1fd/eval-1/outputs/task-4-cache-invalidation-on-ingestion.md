## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM. Without this, the advisory-summary endpoint could serve stale severity counts for up to 5 minutes after new advisory correlations are ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after advisory-SBOM correlation

## Implementation Notes
In the advisory ingestion pipeline at `modules/ingestor/src/graph/advisory/mod.rs`, locate the section where advisories are correlated with SBOMs (after storing advisory data and linking it to affected SBOMs via the `sbom_advisory` join table from `entity/src/sbom_advisory.rs`). After the correlation step, collect the affected SBOM IDs and invalidate their cached advisory-summary responses. Use the same `tower-http` caching infrastructure referenced in the endpoint's cache configuration from Task 3. The `IngestorService` in `modules/ingestor/src/service/mod.rs` may need access to the cache handle to perform invalidation.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Existing advisory ingestion and correlation logic
- `modules/ingestor/src/service/mod.rs::IngestorService` — Service that orchestrates ingestion

## Acceptance Criteria
- [ ] Advisory ingestion invalidates cached advisory-summary for all affected SBOM IDs
- [ ] Cache invalidation occurs only for SBOMs linked to the newly ingested advisory
- [ ] Ingestion pipeline continues to function correctly after adding invalidation logic
- [ ] No performance regression in advisory ingestion throughput

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, verify cached summary is invalidated
- [ ] Integration test: verify unrelated SBOM caches are not invalidated
- [ ] Verify ingestion pipeline completes successfully with cache invalidation enabled

## Verification Commands
- `cargo check -p trustify-ingestor` — compiles without errors
- `cargo test -p trustify-ingestor` — all tests pass

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching