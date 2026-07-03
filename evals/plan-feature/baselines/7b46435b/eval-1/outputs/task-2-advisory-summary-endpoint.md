# Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute caching

## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST API endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns advisory severity counts for a given SBOM. The endpoint calls the service method created in Task 1, returns 404 if the SBOM does not exist, and applies a 5-minute cache using the existing tower-http caching middleware. This is the primary consumer-facing API for the severity aggregation feature.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new advisory-summary route under `/api/v2/sbom/{id}/advisory-summary`
- `server/src/main.rs` — verify route mounting (may require no changes if SBOM module auto-registers sub-routes)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for GET /api/v2/sbom/{id}/advisory-summary

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 OK, or 404 if SBOM not found

## Implementation Notes
- Follow the endpoint pattern established by `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}). The handler should extract the SBOM ID from the path, call `SbomService::get_advisory_severity_summary()`, and return the result as JSON.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint file scope.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing pattern where each endpoint file's handler is registered as a route. See how `get.rs` and `list.rs` are registered.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint registration scope.
- Return `Result<Json<AdvisorySeveritySummary>, AppError>` — consistent with the error handling convention where all handlers return `Result<T, AppError>`.
- For 404 handling: when the SBOM ID does not exist, return `AppError::NotFound` (or equivalent variant from `common/src/error.rs`), consistent with how `modules/fundamental/src/sbom/endpoints/get.rs` handles missing SBOMs.
- Apply 5-minute caching using tower-http caching middleware in the route builder, following the caching configuration pattern used by existing endpoint route builders.
- The response is not paginated (unlike list endpoints that return `PaginatedResults<T>`), so return `Json<AdvisorySeveritySummary>` directly.
- Per constraints doc section 5 (Code Change Rules): implementation must follow the patterns referenced here and inspect existing code before modifying.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — pattern for GET /api/v2/sbom/{id} handler (path extraction, service call, error handling)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — error type with IntoResponse implementation for 404 handling
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — service to call for data retrieval

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with severity counts JSON for a valid SBOM
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 404 when SBOM ID does not exist
- [ ] Response is cached for 5 minutes (subsequent requests within 5 minutes return cached response)
- [ ] Response shape matches `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`

## Test Requirements
- [ ] Integration test: GET with valid SBOM ID returns 200 and correct severity counts
- [ ] Integration test: GET with non-existent SBOM ID returns 404
- [ ] Integration test: verify response JSON structure matches expected shape
- [ ] Integration test: verify caching behavior (second request within 5 minutes is served from cache)

## Verification Commands
- `cargo test --package fundamental -- advisory_summary` — endpoint tests pass
- `cargo check --workspace` — no compilation errors across workspace

## Documentation Updates
- `docs/api/` — add advisory-summary endpoint to REST API reference (path, method, parameters, response shape, error codes)

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
