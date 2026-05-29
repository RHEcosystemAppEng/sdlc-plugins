## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory severity summary for that SBOM is invalidated. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns up-to-date severity counts after new advisory data is ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation step

## Implementation Notes
- The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. Locate the correlation step where advisories are linked to SBOMs via the `sbom_advisory` join table.
- After the correlation step completes, invoke cache invalidation for the affected SBOM IDs. The exact invalidation mechanism depends on how `tower-http` caching is configured in the project — inspect the existing cache setup in `server/src/main.rs` and endpoint route builders to understand the cache key structure.
- If the caching layer uses HTTP-level cache headers (Cache-Control), invalidation may require purging cached responses by key or using cache versioning. If the caching is application-level (e.g., an in-memory cache or Redis), call the appropriate invalidation method.
- Follow the error handling pattern in `modules/ingestor/src/graph/advisory/mod.rs` — use `Result<T, AppError>` with `.context()` wrapping for any new fallible operations.
- Reference `modules/ingestor/src/service/mod.rs` (`IngestorService`) for the overall ingestion service pattern.
- Per docs/constraints.md §5.2: inspect the actual ingestion code before modifying it.
- Per docs/constraints.md §5.1: keep changes scoped to the cache invalidation hook — do not modify unrelated ingestion logic.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion module; extend its correlation step with cache invalidation.
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module; may contain similar post-ingestion hooks that demonstrate the pattern for adding side effects after data correlation.

## Acceptance Criteria
- [ ] Advisory ingestion pipeline invalidates cached advisory severity summary when new advisories are linked to an SBOM
- [ ] Cache invalidation targets only the affected SBOM IDs, not all cached summaries
- [ ] Existing advisory ingestion behavior is not altered beyond the cache invalidation hook
- [ ] Cache invalidation failures are logged but do not block the ingestion pipeline

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, verify that a subsequent GET to `/api/v2/sbom/{id}/advisory-summary` reflects the new advisory (not stale cached data)
- [ ] Integration test: verify that advisory ingestion completes successfully even if cache invalidation encounters an error (graceful degradation)

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching

[sdlc-workflow] Description digest: sha256:1f577920943f9edf47624366bf0f4904b601c08033d7d6eb50d2348183d43fb1
