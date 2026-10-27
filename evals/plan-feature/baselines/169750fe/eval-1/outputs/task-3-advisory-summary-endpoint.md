## Repository
trustify-backend

## Target Branch
main

## Description
Create the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the `advisory_severity_summary` service method and returns the `AdvisorySeveritySummary` response. The response must be cached for 5 minutes using the existing tower-http caching middleware.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler function that extracts the SBOM ID from the path, calls `SbomService::advisory_severity_summary`, and returns the result as JSON with a 5-minute cache header

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route in the route builder

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with 5-minute cache TTL

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`) for path parameter extraction and response handling. The handler should:

1. Extract the SBOM ID from the path using Axum's `Path` extractor.
2. Call `SbomService::advisory_severity_summary(id)`.
3. Return `Json(summary)` on success, or the appropriate error response via `AppError` (which implements `IntoResponse` per `common/src/error.rs`).
4. Add cache control headers for 5-minute TTL using the tower-http caching middleware pattern already in use (see route builders in `modules/fundamental/src/sbom/endpoints/mod.rs`).

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing pattern where routes like `GET /api/v2/sbom/{id}` are registered via the route builder. Mount the new endpoint alongside the existing SBOM routes.

Per CONVENTIONS.md §Endpoint Registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

Per CONVENTIONS.md §Error Handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler file scope.

Per CONVENTIONS.md §Caching: uses tower-http caching middleware; cache configuration in endpoint route builders.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM detail endpoint, demonstrates path parameter extraction and JSON response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern with cache configuration
- `common/src/error.rs::AppError` — standard error handling with IntoResponse

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with severity counts JSON
- [ ] Response includes fields: `critical`, `high`, `medium`, `low`, `total`
- [ ] Response includes cache control headers with 5-minute TTL
- [ ] Returns 404 when SBOM ID does not exist
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Integration test: valid SBOM ID returns correct severity counts
- [ ] Integration test: nonexistent SBOM ID returns 404
- [ ] Verify cache control headers are present in the response

## Verification Commands
- `cargo test --test api` — run integration tests and verify the new endpoint passes

## Dependencies
- Depends on: Task 1 — Advisory severity summary model
- Depends on: Task 2 — Advisory summary service
