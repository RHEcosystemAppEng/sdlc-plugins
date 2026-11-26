## Repository
trustify-backend

## Target Branch
main

## Description
Expose the advisory severity aggregation as a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` (TC-9001). The endpoint returns `{ critical, high, medium, low, total }` for the SBOM, returns 404 when the SBOM ID does not exist (consistent with `GET /api/v2/sbom/{id}`), and caches responses for 5 minutes using the existing caching infrastructure. This replaces the frontend's multi-page fetch of `GET /api/v2/sbom/{id}/advisories` plus client-side counting.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route and attach the 5-minute cache configuration in the route builder
- `tests/api/sbom.rs` — add integration tests for the new endpoint

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler calling `SbomService::advisory_severity_summary` and returning `Json<AdvisorySeveritySummary>`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` (unique advisories only); 404 if the SBOM does not exist; response cached for 5 minutes

## Implementation Notes
- Model the handler on `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`): same path extractor for `{id}`, same service injection, same 404 behavior for unknown IDs. The not-found mapping comes from `common/src/error.rs` (`AppError` implements `IntoResponse`) — do not hand-build a 404 response.
- This is a single-object endpoint, not a list endpoint: return the summary struct directly, not `PaginatedResults<T>`.
- Caching: use the existing `tower-http` caching middleware configured in endpoint route builders (see how existing routes in `modules/fundamental/src/sbom/endpoints/mod.rs` and `modules/fundamental/src/advisory/endpoints/mod.rs` configure caching). Set a TTL / max-age of 300 seconds, scoped to this route only, and ensure the cache key includes the SBOM `{id}` (and the full query string, so Task 4's `threshold` parameter does not collide). Make the cache key format discoverable/reusable (e.g., a `pub fn` or constant) because Task 3 must invalidate entries for a given SBOM ID.
- Do not cache 404 responses (otherwise a newly ingested SBOM would 404 for up to 5 minutes).
- Route is mounted via `server/src/main.rs` through the SBOM module's router; no change to `main.rs` is expected unless the cache handle must be shared (coordinate with Task 3).
- Per CONVENTIONS.md §Endpoint registration: register the route in the module's `endpoints/mod.rs` alongside `list.rs` and `get.rs`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `endpoints/mod.rs` scope. Example: existing `/api/v2/sbom/{id}` registration in the same file.
- Per CONVENTIONS.md §Caching: configure caching in the endpoint route builder using `tower-http` caching middleware. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder scope.
- Per CONVENTIONS.md §Error handling: the handler returns `Result<Json<AdvisorySeveritySummary>, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler (`.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/sbom.rs` against the real PostgreSQL test database, asserting with `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/` integration test scope.
- Constraints (docs/constraints.md): Conventional Commits with Jira ID footer and `Assisted-by:` trailer (§2.1–2.3); PR with `--base main`, link posted on Jira (§3.2, §3.3); scope to listed files, inspect before modifying, no duplicated functionality, sibling parity with `get.rs` for error handling/logging (§5.1–5.8).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — sibling handler for `/api/v2/sbom/{id}`; copy extractor, 404 handling, and service wiring
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration and caching configuration pattern
- `common/src/error.rs::AppError` — not-found response mapping via `IntoResponse`
- `tests/api/sbom.rs` — existing SBOM integration test fixtures/helpers (SBOM ingestion setup, HTTP client)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` for an existing SBOM
- [ ] Counts reflect unique advisories only (deduplicated by advisory ID)
- [ ] Returns 404 for a non-existent SBOM ID, with the same error body shape as `GET /api/v2/sbom/{id}`
- [ ] Successful responses are cached for 5 minutes (300 s) using the existing tower-http caching configuration; 404 responses are not cached
- [ ] Cache key is per SBOM ID (and query string) and is exposed for invalidation by Task 3
- [ ] Existing `/api/v2/sbom` and `/api/v2/sbom/{id}` endpoints are unchanged

## Test Requirements
- [ ] Integration test: SBOM with known advisories of each severity returns expected counts and total
- [ ] Integration test: duplicate advisory links are counted once
- [ ] Integration test: unknown SBOM ID returns 404
- [ ] Integration test: SBOM with no advisories returns all zeros with 200
- [ ] Integration test: response carries the expected cache headers / second request within TTL is served from cache

## Verification Commands
- `cargo test --test api sbom` — new and existing SBOM integration tests pass
- `curl -s http://localhost:8080/api/v2/sbom/<id>/advisory-summary` — returns JSON with `critical`, `high`, `medium`, `low`, `total`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/api/v2/sbom/does-not-exist/advisory-summary` — prints `404`

## Documentation Updates
- `README.md` — if it lists available API endpoints, add `GET /api/v2/sbom/{id}/advisory-summary` (full REST API reference is handled by the documentation task)

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service method
