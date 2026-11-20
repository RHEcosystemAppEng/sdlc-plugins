## Repository
trustify-backend

## Target Branch
main

## Description
Expose the severity aggregation from Task 1 as `GET /api/v2/sbom/{id}/advisory-summary` (TC-9001 MVP). The endpoint returns `{ critical, high, medium, low, total }`, returns 404 when the SBOM does not exist (same as existing SBOM endpoints), and caches responses for 5 minutes using the existing caching infrastructure. This replaces the multi-page client-side counting the dashboard does today.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/advisory-summary` route and configure 5-minute caching on it
- `tests/api/sbom.rs` — add integration tests for the new endpoint

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler calling `SbomService::advisory_severity_summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` for unique advisories linked to the SBOM; 404 if the SBOM does not exist; response cached 5 minutes

## Implementation Notes
- Model the handler on `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`): same path-parameter extraction, same not-found mapping to `AppError` → 404, so the error body matches existing SBOM endpoints.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` next to the existing `list`/`get` routes. `server/src/main.rs` already mounts the SBOM module, so no change is needed there — confirm during implementation.
- Caching: the repo uses `tower-http` caching middleware configured in endpoint route builders. Apply a 5-minute (300s) TTL to this route only. Task 3 has to be able to invalidate these entries when advisories are linked to an SBOM, so build the cache keyed by SBOM ID with an invalidation hook (a shared cache handle that the ingestor can reach). A pure HTTP `Cache-Control: max-age=300` header alone cannot be invalidated server-side. Document the chosen mechanism in the handler module.
- Per CONVENTIONS.md §Endpoint registration: register the route in the module's `endpoints/mod.rs`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration (`endpoints/mod.rs`) scope. Example: `modules/fundamental/src/advisory/endpoints/mod.rs`.
- Per CONVENTIONS.md §Error handling: the handler returns `Result<Json<AdvisorySeveritySummary>, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler (`.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Caching: configure caching in the endpoint route builder with `tower-http` caching middleware. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` against the PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/*.rs` scope. Example: existing tests in `tests/api/sbom.rs`.
- Constraints (docs/constraints.md): §2 commits use Conventional Commits, reference the Jira task ID in the footer, and include an `Assisted-by:` trailer; §3 branch is named after the task ID and the PR is opened with `--base main` with its link posted to Jira; §5 keep changes to the listed files, inspect code before modifying, reuse existing helpers rather than duplicating logic.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing `GET /api/v2/sbom/{id}` handler; template for path extraction and 404 behavior
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration for `/api/v2/sbom`
- `common/src/error.rs::AppError` — `IntoResponse` mapping for 404/500
- `tests/api/sbom.rs` — existing SBOM integration test fixtures and setup helpers

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` for an existing SBOM
- [ ] Returns 404 for a non-existent SBOM ID, with the same error format as `GET /api/v2/sbom/{id}`
- [ ] Responses are cached for 5 minutes (a second request within the TTL is served from cache)
- [ ] The cache is keyed per SBOM ID and exposes an invalidation hook that Task 3 can use
- [ ] Existing `/api/v2/sbom` routes are unchanged

## Test Requirements
- [ ] Integration test in `tests/api/sbom.rs`: seeded SBOM with mixed-severity advisories returns 200 and the expected counts
- [ ] Integration test: duplicate advisory links are counted once in the response
- [ ] Integration test: unknown SBOM ID returns 404
- [ ] Integration test: SBOM with no advisories returns 200 and all zeros
- [ ] Test: a repeated request within the TTL is served from cache (e.g., the underlying data changes without invalidation and the cached value is still returned)

## Verification Commands
- `cargo test --test api sbom` — SBOM integration tests pass
- `curl -s http://localhost:8080/api/v2/sbom/<id>/advisory-summary` — returns the JSON counts object

## Documentation Updates
- `README.md` — mention the new advisory-summary endpoint if the README lists SBOM endpoints (the full API reference update is covered by Task 5)

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service method
