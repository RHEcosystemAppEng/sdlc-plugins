## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that invokes the severity aggregation service method (Task 1) and returns the `AdvisorySeveritySummary` as a JSON response. Configure 5-minute cache headers using the existing tower-http caching middleware. Return 404 when the SBOM ID does not exist, consistent with existing SBOM endpoints.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/advisory-summary` route under the existing `/api/v2/sbom/{id}` path

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for `GET /api/v2/sbom/{id}/advisory-summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 OK, or 404 if SBOM not found

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler function signature, path parameter extraction, dependency injection of the service, and error-to-response mapping.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for `get.rs` and `list.rs` route registration.
- Use tower-http caching middleware for the 5-minute cache. Per repo conventions, cache configuration is set in endpoint route builders. Add `Cache-Control: max-age=300` (5 minutes = 300 seconds) to the route configuration.
- The handler should call the service method from Task 1, map the `AppError` to the appropriate HTTP response (404 for not-found, 500 for internal errors), and serialize the result as JSON.
- Per repo conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM endpoint handler; follow its pattern for path parameter extraction, service injection, and response serialization
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to replicate
- `common/src/error.rs::AppError` — error type that implements `IntoResponse` for automatic HTTP error mapping

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Response includes `Cache-Control: max-age=300` header (5-minute cache)
- [ ] Route is registered in the SBOM module's endpoint configuration

## Test Requirements
- [ ] Integration test: valid SBOM ID returns 200 with correct severity counts
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: response content type is `application/json`
- [ ] Verify cache header is present in response

## Verification Commands
- `cargo test --test api -- advisory_summary` — run integration tests for the new endpoint

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and severity aggregation service method
