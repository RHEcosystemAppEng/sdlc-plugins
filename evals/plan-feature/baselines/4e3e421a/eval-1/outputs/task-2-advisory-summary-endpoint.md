## Repository
trustify-backend

## Target Branch
main

## Description
Expose the advisory severity aggregation as a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` (TC-9001). The endpoint returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` for the given SBOM, returns 404 when the SBOM does not exist (consistent with `GET /api/v2/sbom/{id}`), and caches the response for 5 minutes using the existing caching infrastructure. This replaces the frontend's multi-page fetch of `GET /api/v2/sbom/{id}/advisories` and client-side counting.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/advisory-summary` route and apply the 5-minute cache configuration in the route builder
- `tests/api/sbom.rs` — add integration tests for the new endpoint

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler `get_advisory_summary` that calls `SbomService::advisory_severity_summary` and maps `None` to 404

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `AdvisorySeveritySummary` JSON `{ critical, high, medium, low, total }`; 404 if the SBOM does not exist; response cached for 5 minutes

## Implementation Notes
- Model the handler on `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`): same path-parameter extraction, same service injection, and the same not-found handling so the 404 body/shape is identical to existing SBOM endpoints.
- Handler signature returns `Result<Json<AdvisorySeveritySummary>, AppError>` (`common/src/error.rs`), with `.context(...)` on service errors.
- Do not wrap the response in `PaginatedResults<T>` (`common/src/model/paginated.rs`) — this is a single-object summary, not a list endpoint.
- Route registration: add the route alongside the existing `/api/v2/sbom` routes in `modules/fundamental/src/sbom/endpoints/mod.rs`. `server/src/main.rs` already mounts the SBOM module, so no change is needed there — verify this during implementation.
- Caching: the repo uses `tower-http` caching middleware configured in endpoint route builders. Apply a 5-minute (300s) cache layer to this route only, mirroring how existing routes configure caching. Cache must be keyed by SBOM ID (and, once Task 4 lands, by the `threshold` query param) so different SBOMs never share an entry.
- Cache invalidation hook: expose the cache handle (or a small `invalidate_advisory_summary(sbom_id)` function) in a way Task 3 can call from the ingestor. If the existing `tower-http` configuration only sets HTTP `Cache-Control` headers (client/proxy-side caching) and offers no server-side store that can be invalidated, stop and raise this with the feature owner — the NFR "ingestion must invalidate cached summaries" cannot be satisfied by header-only caching (see impact map, open question).
- 404 must take precedence over the cache: never cache a 404 for an SBOM ID in a way that would keep returning 404 after the SBOM is ingested, and never return a cached zero-count body for a missing SBOM.
- Constraints (docs/constraints.md): §2 Conventional Commits with Jira footer and `Assisted-by: Claude Code` trailer; §3 PR with `--base main`, link posted to Jira; §5 scope to listed files, inspect before modifying, compare with sibling endpoint `get.rs` for parity in error handling and logging.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing `GET /api/v2/sbom/{id}` handler; template for path extraction and 404 behavior
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration and cache configuration pattern
- `common/src/error.rs::AppError` — standard error/404 mapping via `IntoResponse`
- `tests/api/sbom.rs` — existing SBOM integration tests; reuse fixtures/helpers for ingesting a test SBOM with advisories

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with body `{ critical, high, medium, low, total }` for an existing SBOM
- [ ] Counts reflect unique advisories only (deduplicated by advisory ID)
- [ ] Returns 404 for a non-existent SBOM ID, with the same error shape as `GET /api/v2/sbom/{id}`
- [ ] Returns 200 with all-zero counts for an existing SBOM with no advisories (not 404)
- [ ] Response is cached for 5 minutes, keyed per SBOM ID
- [ ] A cache invalidation entry point is available for the ingestor (consumed by Task 3)
- [ ] Existing SBOM endpoints (`GET /api/v2/sbom`, `GET /api/v2/sbom/{id}`) are unchanged

## Test Requirements
- [ ] Integration test in `tests/api/sbom.rs`: SBOM with known advisories returns `StatusCode::OK` and correct counts
- [ ] Integration test: duplicate advisory links are counted once
- [ ] Integration test: non-existent SBOM ID returns `StatusCode::NOT_FOUND`
- [ ] Integration test: SBOM with no advisories returns `StatusCode::OK` with all zeros
- [ ] Integration test: two different SBOMs return their own counts (no cross-SBOM cache bleed)
- [ ] Follow the existing `assert_eq!(resp.status(), StatusCode::OK)` pattern against the PostgreSQL test database

## Verification Commands
- `cargo test --test api sbom` — SBOM integration tests, including new ones, pass
- `curl -s http://localhost:8080/api/v2/sbom/<id>/advisory-summary` — returns JSON with `critical`, `high`, `medium`, `low`, `total`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/api/v2/sbom/does-not-exist/advisory-summary` — prints `404`

## Documentation Updates
- `README.md` — if the README lists API endpoints, add `GET /api/v2/sbom/{id}/advisory-summary` (full API reference update is handled by Task 5)

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service aggregation
