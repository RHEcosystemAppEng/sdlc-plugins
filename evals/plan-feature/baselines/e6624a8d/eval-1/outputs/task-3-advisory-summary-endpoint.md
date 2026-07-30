## Repository
trustify-backend

## Target Branch
main

## Description
Add a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts for a given SBOM. The endpoint delegates to the SbomService aggregation method (Task 2) and applies a 5-minute cache using the existing tower-http caching middleware. This also implements the optional `?threshold` query parameter to filter counts above a given severity level, supporting alerting integrations.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for GET /api/v2/sbom/{id}/advisory-summary with optional threshold query parameter and 5-minute cache configuration

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the advisory-summary route in the SBOM endpoint router

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`. Returns 404 if SBOM ID does not exist. Supports optional `?threshold=critical|high|medium|low` query parameter to filter counts to only those at or above the specified severity level.

## Implementation Notes
- Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) for path parameter extraction, error handling, and response construction.
- Register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing SBOM routes (list.rs, get.rs). Follow the route registration pattern used there.
- Apply tower-http caching middleware with a 5-minute TTL. Reference the existing caching configuration pattern described in the repository conventions for endpoint route builders.
- For the optional `?threshold` query parameter, define a query struct with `threshold: Option<Severity>` where `Severity` is an enum (Critical, High, Medium, Low). When present, filter the response to include only counts at or above the threshold level and recalculate the total.
- Return 404 using `AppError` when the SBOM ID does not exist, consistent with existing SBOM endpoints (see `modules/fundamental/src/sbom/endpoints/get.rs`).
- Per CONVENTIONS.md: register the route in the module's `endpoints/mod.rs` and use `Result<T, AppError>` return type.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` endpoint file scope.
- Per CONVENTIONS.md: use tower-http caching middleware for response caching, configured in endpoint route builders.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET endpoint handler showing path parameter extraction, error handling, and response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for SBOM endpoints
- `common/src/error.rs::AppError` — error enum with IntoResponse implementation for consistent HTTP error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with severity counts JSON
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response is cached for 5 minutes using tower-http caching middleware
- [ ] Optional `?threshold` query parameter filters counts to severities at or above the specified level
- [ ] Route is registered in the SBOM endpoint module alongside existing routes

## Test Requirements
- [ ] Integration test: GET returns 200 with correct severity counts for a valid SBOM
- [ ] Integration test: GET returns 404 for non-existent SBOM ID
- [ ] Integration test: threshold parameter filters results correctly for each severity level
- [ ] Integration test: verify response shape matches `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`

## Verification Commands
- `cargo test --test api advisory_summary` — runs integration tests for the new endpoint

## Documentation Updates
- `README.md` — add the new advisory-summary endpoint to the API overview if one exists

## Dependencies
- Depends on: Task 2 — Add advisory severity aggregation service method
