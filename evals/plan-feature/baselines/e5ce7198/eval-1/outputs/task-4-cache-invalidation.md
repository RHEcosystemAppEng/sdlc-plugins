# Task 4: Add cache invalidation on advisory ingestion

## Repository
trustify-backend

## Target Branch
main

## Description
Modify the advisory ingestion pipeline to invalidate cached advisory summary responses when new advisories are linked to an SBOM. This ensures that the 5-minute cached responses from the advisory summary endpoint are evicted when the underlying data changes, preventing stale severity counts from being served to consumers.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after advisory-SBOM correlation

## Implementation Notes
The advisory ingestion logic in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. After the correlation step (where an advisory is linked to an SBOM via the `sbom_advisory` join table), add a cache invalidation call to evict any cached advisory summary for the affected SBOM ID(s).

The invalidation approach depends on the existing `tower-http` caching infrastructure. Possible strategies:
1. If the cache layer supports key-based invalidation, evict entries matching `/api/v2/sbom/{id}/advisory-summary` for each affected SBOM ID
2. If using a shared cache store (e.g., in-memory map), inject a cache handle into the ingestor service and call a purge method
3. If cache-control is header-based only, consider adding an `ETag` or `Last-Modified` approach where the ingestor updates a version counter that the endpoint checks

Follow the error handling pattern with `Result<T, AppError>` and `.context()` wrapping for any new error paths.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping for all error paths.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion logic to extend with cache invalidation
- `modules/ingestor/src/service/mod.rs::IngestorService` — service struct that may need a cache handle injected

## Acceptance Criteria
- [ ] Advisory ingestion pipeline invalidates cached advisory summary when a new advisory is linked to an SBOM
- [ ] Cache invalidation targets only the affected SBOM ID(s), not all cached summaries
- [ ] Ingestion pipeline continues to function correctly after adding invalidation logic
- [ ] No performance regression in advisory ingestion throughput

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, verify that a subsequent advisory-summary request reflects the new advisory (not a stale cached response)
- [ ] Integration test: ingesting an advisory for SBOM-A does not invalidate cached summary for SBOM-B

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Verification Commands
- `cargo check -p trustify-ingestor` — compiles without errors
- `cargo test -p trustify-ingestor advisory` — ingestion tests pass

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:62899f1f5bfb5320769d054c70494ee2d7232f01a509cdeaf4f17e77a8e2f112
