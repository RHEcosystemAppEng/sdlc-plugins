## Repository
trustify-backend

## Target Branch
main

## Description
Modify the advisory ingestion pipeline to invalidate cached advisory-summary responses when new advisories are linked to an SBOM. Currently, the advisory ingestion module parses, stores, and correlates advisories with SBOMs. After the correlation step links a new advisory to an SBOM, the cached `GET /api/v2/sbom/{id}/advisory-summary` response for that SBOM must be invalidated so subsequent requests return updated severity counts. Without this, the 5-minute cache could serve stale data after new advisory ingestion.

This satisfies the non-functional requirement in Feature TC-9001: "advisory ingestion pipeline must invalidate cached summaries when new advisories are linked to an SBOM."

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation logic after advisory-SBOM correlation step; invalidate the advisory-summary cache entry for each affected SBOM ID

## Implementation Notes
- The advisory ingestion flow in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. The correlation step links advisories to SBOMs via the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`).
- After the correlation step completes (where new `sbom_advisory` rows are inserted), collect the affected SBOM IDs and invalidate their advisory-summary cache entries.
- Use the `tower-http` cache invalidation mechanism consistent with how caching was set up in Task 2. If the cache is keyed by request path (e.g., `/api/v2/sbom/{id}/advisory-summary`), invalidate entries for each affected SBOM ID.
- Reference `modules/ingestor/src/graph/sbom/mod.rs` for the existing SBOM ingestion pattern to understand how the ingestion pipeline is structured.
- Reference `modules/ingestor/src/service/mod.rs` (`IngestorService`) for the service layer that orchestrates ingestion.
- Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for any fallible cache invalidation operations. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's service file scope.
- Per docs/constraints.md §5 (Code Change Rules): changes scoped to the listed file; reuse existing cache infrastructure.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion logic to extend with cache invalidation
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pattern for reference on pipeline structure
- `entity/src/sbom_advisory.rs` — join table entity used during correlation; provides SBOM IDs for cache invalidation

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` calls after ingestion return updated counts reflecting the newly linked advisory
- [ ] Cache invalidation targets only the specific SBOM IDs affected by the ingestion, not all cached entries
- [ ] Cache invalidation does not introduce errors or break the existing advisory ingestion flow

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, then verify the advisory-summary endpoint returns updated counts (not stale cached data)
- [ ] Integration test: verify that cache invalidation for one SBOM does not affect the cached advisory-summary for a different SBOM
- [ ] Integration test: verify the advisory ingestion pipeline completes successfully with cache invalidation enabled

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
