# Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache

**Summary:** TC-9001: Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 404 handling and 5-minute caching
**Issue type:** Task
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9001)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9001)

---

## Repository
trustify-backend

## Target Branch
main

## Description
Expose the severity aggregation from Task 1 as a new REST endpoint, `GET /api/v2/sbom/{id}/advisory-summary`. It returns `{ critical: N, high: N, medium: N, low: N, total: N }` for the given SBOM and returns 404 when the SBOM does not exist, the same way existing SBOM endpoints do. Responses are cached for 5 minutes using the existing cache infrastructure. The cache is keyed per SBOM ID so the ingestion pipeline (Task 3) can invalidate one SBOM's entry when new advisories are linked to it.

This replaces the multi-page `GET /api/v2/sbom/{id}/advisories` fetch-and-count the dashboard does today (UC-1). Part of feature TC-9001.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/advisory-summary` route and attach the 5-minute cache configuration in the route builder
- `tests/api/sbom.rs` — add integration tests for the new endpoint

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler: parse `{id}`, call `SbomService::advisory_severity_summary`, map `None` to the 404 `AppError`, and return `Json<AdvisorySeveritySummary>`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `200 { critical: u64, high: u64, medium: u64, low: u64, total: u64 }`, returns `404` if the SBOM ID does not exist, and is cached for 300 seconds

## Implementation Notes
- Handler: copy the structure of `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`). Use the same path extractor, service injection, and not-found mapping so the 404 body and status match existing SBOM endpoints exactly.
- Routing: register the handler in `modules/fundamental/src/sbom/endpoints/mod.rs` next to the `list.rs` and `get.rs` routes. `server/main.rs` already mounts the SBOM module router, so no change is needed there. Confirm this, and only touch `server/main.rs` if the module router is not mounted wholesale.
- Caching: the repo uses `tower-http` caching middleware configured in endpoint route builders. Apply a 300-second TTL to this route only, so other SBOM routes keep their current behaviour. The cache key must include the SBOM ID. Expose a public invalidation function (for example `invalidate_advisory_summary(sbom_id)`) next to the cache setup so Task 3 can call it from the ingestor.
- **Open question:** if the existing `tower-http` setup only sets HTTP `Cache-Control` headers (client or proxy caching) and has no server-side store, it cannot be invalidated from the ingestion pipeline, so the cache-invalidation NFR could not be met. Check this first. If the setup is header-only, stop and raise it on TC-9001 before adding a new dependency (the feature says "use existing cache infrastructure").
- Response type: return the bare `AdvisorySeveritySummary` object, not `PaginatedResults<T>` (`common/src/model/paginated.rs`). `PaginatedResults` is only for list endpoints.
- If sibling handlers have OpenAPI annotations (`#[utoipa::path]`), add one so the endpoint shows up in the generated spec.
- Per CONVENTIONS.md §Endpoint registration: register the route in the module's `endpoints/mod.rs`. `server/main.rs` mounts all modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `endpoints/mod.rs` route-registration scope.
- Per CONVENTIONS.md §Caching: configure the 5-minute cache in the endpoint route builder with the existing `tower-http` caching middleware. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route-builder scope.
- Per CONVENTIONS.md §Error handling: the handler returns `Result<Json<AdvisorySeveritySummary>, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler `.rs` scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/sbom.rs` against the real PostgreSQL test database, using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/` integration-test scope.
- Constraints (docs/constraints.md): §5.1 scope is limited to the files above. §5.2 inspect `get.rs` and `mod.rs` before editing. §5.3 follow the `get.rs` pattern. §5.4 reuse the existing not-found mapping and cache middleware. §5.8 match sibling SBOM endpoints on error handling, logging, and auth. §5.11–5.13 add doc comments to every test function, and given-when-then comments to non-trivial tests. §2.1–2.3 and §3.1–3.3 apply to commits and PRs (task key in the footer, Conventional Commits, `Assisted-by:` trailer, `--base main`).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing `GET /api/v2/sbom/{id}` handler. Copy its path parsing and 404 mapping.
- `common/src/error.rs::AppError` — existing not-found variant and `IntoResponse` implementation for consistent 404s.
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route builder and `tower-http` cache configuration pattern.
- `tests/api/sbom.rs` — existing SBOM integration test fixtures (SBOM ingestion helpers, test client) to reuse for seeding data.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` for an existing SBOM
- [ ] Counts are deduplicated by advisory ID
- [ ] Returns 404 for a non-existent SBOM ID, with the same error body shape as `GET /api/v2/sbom/{id}`
- [ ] Response is cached for 5 minutes (TTL 300s), keyed by SBOM ID, and the cache applies only to this route
- [ ] A public per-SBOM cache invalidation function exists for Task 3 to call
- [ ] Existing SBOM routes (`GET /api/v2/sbom`, `GET /api/v2/sbom/{id}`) behave exactly as before

## Test Requirements
- [ ] Integration test: seed an SBOM with advisories at each severity and assert status 200 and the exact counts
- [ ] Integration test: seed duplicate links for one advisory and assert it is counted once
- [ ] Integration test: request an unknown SBOM ID and assert 404
- [ ] Integration test: request an existing SBOM with no advisories and assert all zeros
- [ ] Integration test: assert the response carries the 300-second cache configuration (header or cache hit on a second request, depending on the mechanism)
- [ ] Integration test: call the invalidation function and assert the next request recomputes the counts

## Verification Commands
- `cargo test --test api sbom::advisory_summary` (adjust to the test harness layout in `tests/Cargo.toml`) — all new tests pass
- `curl -s -i http://localhost:8080/api/v2/sbom/<existing-id>/advisory-summary` — `200` with a JSON body containing `critical`, `high`, `medium`, `low`, `total`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/api/v2/sbom/does-not-exist/advisory-summary` — `404`

## Documentation Updates
- `README.md` — if it lists API endpoints, add `GET /api/v2/sbom/{id}/advisory-summary`. The full REST API reference update is covered by Task 5.

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and SbomService aggregation query
