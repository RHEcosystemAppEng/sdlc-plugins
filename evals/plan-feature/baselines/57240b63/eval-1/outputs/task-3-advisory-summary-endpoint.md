## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns advisory severity counts for a given SBOM. The endpoint calls the `SbomService::get_advisory_summary` method and returns the `AdvisorySeveritySummary` as JSON. It includes a 5-minute cache TTL using the existing `tower-http` caching middleware and returns 404 when the SBOM ID does not exist, consistent with existing SBOM endpoints.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function for the advisory summary endpoint; extracts SBOM ID from path, calls service, returns JSON response with cache headers

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 5-minute cache, 404 if SBOM not found

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (the `GET /api/v2/sbom/{id}` handler) for path parameter extraction, service injection, and error handling. Use the same `Path<Uuid>` extractor pattern and `Result<Json<T>, AppError>` return type.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern — add a `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::handler))` entry alongside the existing SBOM routes.
- Apply `tower-http` caching middleware with a 5-minute (300 second) TTL per the caching convention. Reference the existing cache configuration pattern in the endpoint route builders (Key Conventions §Caching).
- Return `Json(summary)` on success and propagate `AppError` from the service layer — the `AppError` enum in `common/src/error.rs` already implements `IntoResponse` for Axum.
- Per Key Conventions §Error handling: handler returns `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` endpoint file scope.
- Per Key Conventions §Endpoint registration: register the route in `endpoints/mod.rs` and ensure it is mounted via `server/src/main.rs`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference implementation for SBOM detail endpoint handler; follow its path extraction and service call pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration to follow for adding the new route
- `common/src/error.rs::AppError` — error type implementing `IntoResponse` for 404 and 500 responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Returns 404 when SBOM ID does not exist, consistent with `GET /api/v2/sbom/{id}`
- [ ] Response includes cache headers with a 5-minute TTL
- [ ] Response time p95 < 200ms for SBOMs with up to 500 advisories

## Test Requirements
- [ ] Integration test: verify 200 response with correct severity counts for an SBOM with known advisories
- [ ] Integration test: verify 404 response for non-existent SBOM ID
- [ ] Integration test: verify cache headers are present with 5-minute TTL

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-tests -- sbom` — integration tests pass

## Dependencies
- Depends on: Task 2 — Add advisory severity aggregation query to SbomService

## Jira Fields
- **Labels:** ai-generated-jira
- **Priority:** Major
- **Fix Versions:** RHTPA 1.5.0

[sdlc-workflow] Description digest: sha256-md:85a959dddc6b993cc45b4678ceb49110bcefbb97d60c5d88fa3ea25bbbb7181f
