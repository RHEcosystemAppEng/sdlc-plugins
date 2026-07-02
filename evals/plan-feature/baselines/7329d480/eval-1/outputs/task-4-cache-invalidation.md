# Task 4 — Invalidate advisory summary cache on advisory ingestion

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }

## Repository
trustify-backend

## Target Branch
main

## Description
Update the advisory ingestion pipeline to invalidate cached advisory summaries when new advisories are linked to an SBOM. Without this, the `GET /api/v2/sbom/{id}/advisory-summary` endpoint could serve stale severity counts for up to 5 minutes after new advisories are ingested. This fulfills the non-functional requirement in TC-9001: "advisory ingestion pipeline must invalidate cached summaries when new advisories are linked to an SBOM."

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation completes

## Implementation Notes
The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. After the step that links an advisory to one or more SBOMs (likely inserting into the `sbom_advisory` join table via `entity/src/sbom_advisory.rs`), add a call to invalidate the cached advisory summary for each affected SBOM ID.

The invalidation mechanism depends on how `tower-http` caching is configured:
- If using an in-memory cache layer (e.g., `tower-http`'s `CacheLayer` with a shared store), call the cache store's invalidation/eviction method for the relevant cache key (the SBOM ID or the full endpoint path).
- If using HTTP cache-control headers only (no server-side cache store), this task may need to introduce a lightweight in-process cache (e.g., `moka` or a `DashMap` with TTL) at the service layer that the ingestion pipeline can invalidate.

Locate the exact point in the ingestion flow where `sbom_advisory` rows are inserted and add the invalidation call immediately after. The affected SBOM IDs are available at that point from the ingestion context.

Per CONVENTIONS.md §Module pattern: the change stays within the ingestor module's existing structure.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's module directory pattern.

Per CONVENTIONS.md §Error handling: wrap any cache invalidation errors with `.context()` and handle gracefully (cache invalidation failure should log a warning but not fail the ingestion).
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` error-handling scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion logic; the invalidation call is added to the existing correlation flow
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for how SBOM ingestion handles post-processing steps
- `entity/src/sbom_advisory.rs` — join table entity; the point where new rows are inserted is the trigger for invalidation

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM during ingestion, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` calls after ingestion return updated counts
- [ ] Cache invalidation failure does not cause the advisory ingestion to fail (graceful degradation)
- [ ] Existing advisory ingestion behavior is unchanged (no regressions)

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, verify that the advisory summary endpoint reflects the updated counts without waiting for cache TTL expiry
- [ ] Integration test: verify that advisory ingestion succeeds even if cache invalidation encounters an error (mock or simulate a failure)

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
