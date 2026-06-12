# Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Register a new HTTP endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts for a given SBOM. The endpoint validates the SBOM ID, calls the service method, applies 5-minute cache headers via `tower-http` caching middleware, and returns the `AdvisorySeveritySummary` as JSON. It also supports an optional `?threshold=critical|high|medium|low` query parameter to filter severity counts.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for `GET /api/v2/sbom/{id}/advisory-summary` with query parameter extraction and cache configuration

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — add route registration for `/api/v2/sbom/{id}/advisory-summary` pointing to the new handler, add `mod advisory_summary;` declaration

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 OK
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: returns filtered counts (only severities at or above threshold)
- Returns 404 if SBOM ID does not exist

## Implementation Notes
- Follow the endpoint pattern established by `modules/fundamental/src/sbom/endpoints/get.rs` (the `GET /api/v2/sbom/{id}` handler). This handler extracts a path parameter for the SBOM ID, calls a service method, and returns the result as JSON with proper error mapping.
- Follow the route registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` which uses Axum's `Router` to mount handlers. Add the new route as `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::handler))` or following the existing route definition pattern.
- **Query parameter extraction**: Use Axum's `Query<T>` extractor for the optional `threshold` parameter. Define a small query params struct (e.g., `AdvisorySummaryParams { threshold: Option<String> }`) and parse the threshold value into the severity enum.
- **Cache configuration**: Use `tower-http` caching middleware to set `Cache-Control: max-age=300` (5 minutes) on the response. Follow the existing caching patterns referenced in the Key Conventions section of the repository structure.
- **Error handling**: Return `Result<Json<AdvisorySeveritySummary>, AppError>` following the convention where all handlers return `Result<T, AppError>` with `.context()` wrapping.
- **Invalid threshold values**: Return 400 Bad Request if the threshold parameter contains an unrecognized severity value.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — established pattern for SBOM detail endpoint handlers with path parameter extraction and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for SBOM endpoints
- `common/src/error.rs::AppError` — error enum implementing `IntoResponse` for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Returns 404 when SBOM ID does not exist, consistent with `GET /api/v2/sbom/{id}`
- [ ] Supports optional `?threshold=critical|high|medium|low` query parameter
- [ ] Returns 400 for invalid threshold values
- [ ] Response includes `Cache-Control: max-age=300` header for 5-minute caching
- [ ] Endpoint is registered and accessible in the Axum router

## Test Requirements
- [ ] Integration test: successful response with correct JSON shape for an SBOM with advisories
- [ ] Integration test: 404 response for non-existent SBOM ID
- [ ] Integration test: threshold query parameter returns filtered counts
- [ ] Integration test: invalid threshold value returns 400
- [ ] Integration test: verify `Cache-Control` header is present with correct max-age

## Verification Commands
- `cargo test --package tests -- api::advisory_summary` — verify all integration tests pass
- `cargo clippy --all-targets` — verify no lint warnings in new code

## Dependencies
- Depends on: Task 2 — Add advisory severity aggregation query to SbomService
