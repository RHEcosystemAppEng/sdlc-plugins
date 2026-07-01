# Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Create the HTTP handler for `GET /api/v2/sbom/{id}/advisory-summary` that returns advisory severity counts for a given SBOM. The handler calls the `SbomService::advisory_severity_summary` method and returns the result as JSON. The route must be registered with 5-minute cache headers using the existing `tower-http` caching middleware, and must support an optional `?threshold` query parameter for filtering counts above a severity level.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for the advisory-summary endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route with cache configuration

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 5-minute cache headers
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: returns only counts at or above the specified severity threshold

## Implementation Notes
- Follow the existing endpoint pattern established by `get.rs` (`GET /api/v2/sbom/{id}`) and `list.rs` (`GET /api/v2/sbom`) in `modules/fundamental/src/sbom/endpoints/`
- The handler function should accept the SBOM ID as a path parameter and call `SbomService::advisory_severity_summary`
- Return `Result<Json<AdvisorySeveritySummary>, AppError>` consistent with other handlers that use `.context()` wrapping from `common/src/error.rs`
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing SBOM routes — this file handles route registration for the `/api/v2/sbom` prefix
- Configure 5-minute caching using `tower-http` caching middleware — reference the existing cache configuration pattern in endpoint route builders
- The `?threshold` query parameter is non-MVP but should be included: accept an optional query parameter with values `critical`, `high`, `medium`, `low` and filter the response to only include counts at or above that severity level
- Return 404 if the SBOM ID does not exist (propagated from the service layer's `AppError`)
- The `server/src/main.rs` mounts all modules — no changes needed there since this is a sub-route of the existing `/api/v2/sbom` mount

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler for SBOM details, showing path parameter extraction and service invocation pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern with existing SBOM routes
- `modules/fundamental/src/sbom/endpoints/list.rs` — shows query parameter handling pattern
- `common/src/error.rs::AppError` — error type with `IntoResponse` for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with severity counts
- [ ] Response includes `critical`, `high`, `medium`, `low`, and `total` fields
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response has 5-minute cache headers configured
- [ ] Optional `?threshold` query parameter filters counts to only include severities at or above the threshold
- [ ] Route is registered in the SBOM endpoints module

## Test Requirements
- [ ] Integration test: valid SBOM ID returns 200 with correct severity count JSON shape
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: `?threshold=critical` returns only critical count
- [ ] Integration test: `?threshold=high` returns critical and high counts
- [ ] Integration test: response includes appropriate cache headers

## Verification Commands
- `cargo test --test api advisory_summary` — expected: all advisory-summary integration tests pass
- `cargo build` — expected: clean compilation with no errors

## Dependencies
- Depends on: Task 2 — Add severity aggregation query to SbomService
