## Repository
trustify-backend

## Target Branch
main

## Description
Expose the advisory severity aggregation as a REST endpoint, `GET /api/v2/sbom/{id}/advisory-summary`, so the dashboard severity widget (TC-9001, UC-1) can render severity breakdowns with a single call instead of paging through `GET /api/v2/sbom/{id}/advisories` and counting client-side. The endpoint returns 404 for unknown SBOM IDs (consistent with existing SBOM endpoints) and caches responses for 5 minutes using the existing cache infrastructure.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/advisory-summary` route with a 5-minute cache configuration in the route builder
- `tests/api/sbom.rs` — add integration tests for the new endpoint

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler calling `SbomService::advisory_severity_summary` and returning `AdvisorySeveritySummary` as JSON

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` counting unique advisories per severity; 404 if the SBOM does not exist; cached for 5 minutes

## Implementation Notes
- Model the handler on `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`): same path-parameter extraction for `{id}`, same 404 behavior via `AppError` from `common/src/error.rs` (`IntoResponse`).
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside `list.rs` and `get.rs`. `server/src/main.rs` already mounts the SBOM module routes, so it should not need changes — verify this during implementation.
- Caching: the repo uses `tower-http` caching middleware configured in endpoint route builders. Apply a 5-minute (300 s) TTL to this route only. The cache key must include the SBOM ID (and, once Task 4 lands, the `threshold` query parameter).
- Before implementing, verify the existing cache infrastructure supports keyed server-side entries that can be invalidated (required by Task 3). If it only emits HTTP `Cache-Control` headers, stop and raise this on the Jira task — do not ship a header-only cache, since ingestion-time invalidation (NFR) would silently not work and stale counts would be served for up to 5 minutes. Expose a small invalidation function (e.g., `invalidate_advisory_summary(sbom_id)`) next to the cache configuration so Task 3 can call it.
- Do not use `PaginatedResults<T>` — this is a single-object aggregate response, not a list.
- Per CONVENTIONS.md §Endpoint registration: register the route in the module's `endpoints/mod.rs`; `server/src/main.rs` mounts the module. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `endpoints/mod.rs` scope.
- Per CONVENTIONS.md §Error handling: the handler returns `Result<Json<AdvisorySeveritySummary>, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler (`.rs`) scope.
- Per CONVENTIONS.md §Caching: configure caching in the endpoint route builder using the existing `tower-http` caching middleware. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/` scope.
- Constraints (docs/constraints.md): §2 commits use Conventional Commits, reference the Jira task in the footer, and include an `Assisted-by:` trailer; §3 PR branch named after the Jira task ID, `gh pr create --base main`, PR link posted on the Jira task; §5 keep changes scoped to the listed files, inspect code before modifying it, reuse existing helpers, and compare against sibling endpoints (`get.rs`, `list.rs`) for parity in error handling and logging.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing `{id}` path handling and 404 pattern to mirror
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration and any existing cache configuration in route builders
- `common/src/error.rs::AppError` — not-found error mapping to HTTP 404
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::advisory_severity_summary` — added in Task 1

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` for an existing SBOM
- [ ] Counts reflect unique advisories (deduplicated by advisory ID)
- [ ] Returns 404 for a non-existent SBOM ID (not 200 with zero counts)
- [ ] Response is cached for 5 minutes, keyed per SBOM ID
- [ ] A keyed invalidation entry point exists for Task 3 to call
- [ ] Existing SBOM endpoints (`GET /api/v2/sbom`, `GET /api/v2/sbom/{id}`) are unchanged

## Test Requirements
- [ ] Integration test: ingest an SBOM with advisories of mixed severities; endpoint returns 200 and correct counts
- [ ] Integration test: duplicate SBOM–advisory links are counted once
- [ ] Integration test: unknown SBOM ID returns 404
- [ ] Integration test: SBOM with no advisories returns 200 with all zeros
- [ ] Integration test: a second request within the TTL is served from cache (or the cache layer is hit), and calling the invalidation function forces a recomputation

## Verification Commands
- `cargo test --test api sbom` — SBOM integration tests, including new advisory-summary tests, pass (adjust to the test target in `tests/Cargo.toml`)
- `curl -s http://localhost:8080/api/v2/sbom/<id>/advisory-summary` — returns the JSON severity summary
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/api/v2/sbom/does-not-exist/advisory-summary` — prints `404`

## Documentation Updates
- `README.md` — if the README lists API endpoints, add `GET /api/v2/sbom/{id}/advisory-summary` (full reference is covered by the documentation task)

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service aggregation
