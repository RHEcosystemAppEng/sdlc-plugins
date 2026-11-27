Summary: Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute caching
Epic: TC-9001: Advisory severity summary endpoint
Labels: ai-generated-jira | Priority: Major | Fix Version: RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Expose the advisory severity aggregation (Task 1) via a new REST endpoint
`GET /api/v2/sbom/{id}/advisory-summary` for TC-9001. Dashboard widgets (UC-1) call this once
instead of paging through `GET /api/v2/sbom/{id}/advisories` and counting client-side. The
endpoint returns 404 for unknown SBOM IDs (consistent with existing SBOM endpoints) and its
responses are cached for 5 minutes using the existing cache infrastructure. The cache must be
keyed per SBOM so Task 3 can invalidate individual entries.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/{id}/advisory-summary` route on the existing `/api/v2/sbom` router with 5-minute cache configuration
- `tests/api/sbom.rs` — integration tests for the new endpoint

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler for `GET /api/v2/sbom/{id}/advisory-summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `AdvisorySeveritySummary` `{ critical: number, high: number, medium: number, low: number, total: number }`; 404 if the SBOM does not exist; cached for 5 minutes

## Implementation Notes
- Handler: follow `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`) for path extraction, service injection, 404 mapping, and response type. Call `SbomService::advisory_severity_summary` from Task 1 and return it as JSON.
- Route registration: add the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside `list` and `get`. `server/src/main.rs` already mounts the SBOM router, so it should not need changes — verify this.
- Caching: configure the 5-minute TTL in the route builder per the repo's caching convention (tower-http caching middleware). **Verify the existing cache infrastructure is a server-side cache that supports per-key invalidation.** If it only emits HTTP `Cache-Control` headers, server-side invalidation (Task 3) is impossible — in that case use/extend the existing server-side cache keyed by SBOM ID, and raise the gap on the Jira task before proceeding rather than shipping a header-only cache. Expose the cache key construction (e.g., `advisory_summary_cache_key(sbom_id)`) as a reusable function so Task 3 invalidates exactly the same key.
- Fail-closed: 404 responses must not be cached as a zero-count summary; an error from the service must surface as an error status, never as a 200 with zeros.
- OpenAPI: if sibling handlers carry `utoipa` path annotations, add matching annotations so the endpoint appears in the generated spec.
- Per CONVENTIONS.md §Endpoint registration: register the route in the SBOM module's `endpoints/mod.rs`; do not mount it directly in `server/src/main.rs`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration (`endpoints/mod.rs`) scope. Example: existing `list`/`get` registration in the same file.
- Per CONVENTIONS.md §Error handling: handler returns `Result<Json<AdvisorySeveritySummary>, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler (`.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Caching: configure caching in the endpoint route builder using the existing `tower-http` caching middleware. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` against the real PostgreSQL test DB using `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/sbom.rs` matching the convention's integration test (`tests/api/*.rs`) scope. Example: existing tests in `tests/api/sbom.rs`.
- Constraints (docs/constraints.md):
  - §1.4/§5.1 — scope limited to the files listed above.
  - §1.5/§5.2 — inspect `get.rs`, `endpoints/mod.rs` and the caching setup before modifying.
  - §5.6 — trace the full path request → handler → service → DB → cache → response.
  - §5.8 — match sibling handlers on error handling, logging and OpenAPI annotations.
  - §5.11–5.13 — doc comments on every new test; given-when-then for non-trivial tests.
  - §2.1–2.3 — Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer.
  - §3.1–3.3 — branch named after the task key; `gh pr create --base main`; post PR link to Jira.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — single-SBOM handler pattern including 404 behavior
- `modules/fundamental/src/sbom/endpoints/mod.rs` — router where existing SBOM routes and cache config live
- `common/src/error.rs::AppError` — `IntoResponse` mapping for 404
- `tests/api/sbom.rs` — existing SBOM integration test setup/fixtures

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` for an existing SBOM
- [ ] Counts reflect unique advisories (dedup by advisory ID)
- [ ] Returns 404 for a nonexistent SBOM ID (never 200 with zeros)
- [ ] Responses are cached for 5 minutes, keyed per SBOM ID, using the existing cache infrastructure
- [ ] Cache key construction is exposed for reuse by the invalidation logic (Task 3)
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Existing SBOM endpoints are unaffected

## Test Requirements
- [ ] Integration test: SBOM with mixed-severity advisories returns 200 and correct counts
- [ ] Integration test: duplicated SBOM–advisory relationships are counted once
- [ ] Integration test: unknown SBOM ID returns 404 (asserts status, not body zeros)
- [ ] Integration test: SBOM with no advisories returns 200 with all zeros
- [ ] Integration test: second request within TTL is served from cache (e.g., add an advisory link directly in DB without invalidation and assert the cached value is returned)
- [ ] Integration test: 404 for an unknown ID is not cached as a success (create the SBOM after a 404 and verify the next call returns 200)

## Verification Commands
- `cargo test -p tests sbom` — all SBOM integration tests pass, including new advisory-summary tests
- `curl -s http://localhost:8080/api/v2/sbom/<existing-id>/advisory-summary` — JSON with `critical`, `high`, `medium`, `low`, `total`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/api/v2/sbom/does-not-exist/advisory-summary` — `404`

## Documentation Updates
- `README.md` — if it lists available API endpoints, add `GET /api/v2/sbom/{id}/advisory-summary` (full REST API reference update is handled by Task 5)

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service method
