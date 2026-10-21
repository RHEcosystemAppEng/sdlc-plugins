## Repository
trustify-backend

## Target Branch
main

## Description
Add the GET /api/v2/sbom/{id}/advisory-summary endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the SbomService aggregation method (Task 1), returns the AdvisorySeveritySummary as JSON, and applies a 5-minute cache TTL using tower-http caching middleware. Returns 404 when the SBOM ID does not exist, consistent with existing SBOM endpoints.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` -- Axum handler function for GET /api/v2/sbom/{id}/advisory-summary; extracts SBOM ID from path, calls SbomService::get_advisory_summary, returns JSON response or 404

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the advisory-summary route under /api/v2/sbom/{id}/advisory-summary with 5-minute cache layer
- `tests/api/sbom.rs` -- add integration tests for the advisory-summary endpoint

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 OK, or 404 if SBOM not found

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction (SBOM ID as `Path<Uuid>`), service injection, and error-to-response mapping.
- Apply tower-http cache middleware with a 300-second (5-minute) TTL on the route builder, following the caching pattern described in CONVENTIONS.md. See existing route registration in `modules/fundamental/src/sbom/endpoints/mod.rs` for how cache layers are applied.
- The handler should return `Result<Json<AdvisorySeveritySummary>, AppError>`. When `SbomService::get_advisory_summary` returns an error for a non-existent SBOM, map it to a 404 response using the AppError enum from `common/src/error.rs`.
- Register the route in the SBOM module's `endpoints/mod.rs` alongside the existing `/api/v2/sbom/{id}` and `/api/v2/sbom` routes.
- Integration tests should follow the pattern in `tests/api/sbom.rs` -- use a test database, insert test SBOMs and advisories, call the endpoint, and assert response status and body content. Use `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- Per CONVENTIONS.md §Endpoint Registration: register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` and ensure the SBOM module mount in `server/src/main.rs` picks it up automatically. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration file scope.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` from the handler, wrapping service errors with `.context()`. See `modules/fundamental/src/sbom/endpoints/get.rs` for the established pattern. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler file scope.
- Per CONVENTIONS.md §Caching: apply tower-http caching middleware on the route builder with a 5-minute TTL. See `modules/fundamental/src/sbom/endpoints/mod.rs` for existing cache configuration patterns. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/sbom.rs` using a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's test file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- existing GET handler for /api/v2/sbom/{id} demonstrating path extraction, service call, and error handling pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- route registration pattern with cache layer configuration
- `common/src/error.rs::AppError` -- error type implementing IntoResponse for automatic HTTP status mapping
- `tests/api/sbom.rs` -- existing SBOM integration tests demonstrating test database setup and assertion patterns

## Acceptance Criteria
- [ ] GET /api/v2/sbom/{id}/advisory-summary returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` for a valid SBOM
- [ ] GET /api/v2/sbom/{id}/advisory-summary returns 404 when the SBOM ID does not exist
- [ ] Response is cached for 5 minutes (300 seconds) using tower-http cache middleware
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Integration tests cover: successful response with correct counts, 404 for missing SBOM, and cache header presence

## Test Requirements
- [ ] Integration test: call GET /api/v2/sbom/{id}/advisory-summary with a valid SBOM that has advisories at multiple severity levels; verify 200 and correct counts
- [ ] Integration test: call GET /api/v2/sbom/{id}/advisory-summary with a valid SBOM that has no advisories; verify 200 and all counts are zero
- [ ] Integration test: call GET /api/v2/sbom/{id}/advisory-summary with a non-existent SBOM ID; verify 404
- [ ] Integration test: verify cache headers are present in the response (Cache-Control max-age=300)

## Dependencies
- Depends on: Task 1 -- Add AdvisorySeveritySummary model and aggregation service method
