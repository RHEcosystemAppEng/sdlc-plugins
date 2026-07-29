## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns advisory severity counts for a given SBOM. The endpoint calls the `SbomService::get_advisory_severity_summary` method (from Task 1), returns the `AdvisorySeveritySummary` as JSON, and configures a 5-minute `tower-http` cache on the response. Returns 404 if the SBOM ID does not exist, consistent with existing SBOM endpoints.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with 5-minute cache; 404 if SBOM not found

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for the handler function signature, path parameter extraction, and error handling.
- Route registration follows the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — add the new route alongside existing SBOM routes.
- Configure 5-minute caching using `tower-http` caching middleware, consistent with the project's caching approach described in the Key Conventions.
- The handler should extract the SBOM ID from the path, call `SbomService::get_advisory_severity_summary`, and return the result as JSON.
- Error handling: return `Result<Json<AdvisorySeveritySummary>, AppError>` following the convention that all handlers return `Result<T, AppError>`.
- Per Key Conventions: endpoint registration pattern — each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per Key Conventions: error handling — all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint file scope.
- Per Key Conventions: caching — uses `tower-http` caching middleware. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint caching scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing `GET /api/v2/sbom/{id}` handler; follow its pattern for path parameter extraction and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — shared error type; use `IntoResponse` impl for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` for a valid SBOM
- [ ] Returns 404 with appropriate error body when SBOM ID does not exist
- [ ] Response includes cache headers indicating 5-minute cache duration
- [ ] Route is registered in `endpoints/mod.rs` alongside existing SBOM routes
- [ ] Response content type is `application/json`

## Test Requirements
- [ ] Integration test: valid SBOM returns 200 with correct severity counts
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: response headers include cache control with 5-minute max-age

## Verification Commands
- `cargo build -p fundamental` — compiles without errors
- `cargo test -p fundamental` — all existing and new tests pass

## Documentation Updates
- REST API reference documentation — add `GET /api/v2/sbom/{id}/advisory-summary` endpoint with path parameters, response shape, cache behavior, and error responses

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service layer
