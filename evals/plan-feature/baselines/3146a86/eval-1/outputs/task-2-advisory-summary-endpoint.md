# Task 2 -- Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns advisory
severity counts for a given SBOM. The endpoint calls the `advisory_severity_summary`
service method (Task 1) and returns the result as JSON. It returns 404 if the SBOM ID
does not exist. The endpoint includes 5-minute cache configuration using the existing
tower-http caching middleware.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the new advisory-summary route alongside existing SBOM routes
- `server/src/main.rs` -- verify the SBOM module route mount already covers the new sub-route (likely no change needed, but confirm)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` -- handler for `GET /api/v2/sbom/{id}/advisory-summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 OK, or 404 if SBOM not found

## Implementation Notes
- Follow the endpoint pattern established by `modules/fundamental/src/sbom/endpoints/get.rs` (the existing `GET /api/v2/sbom/{id}` handler). The handler should:
  1. Extract the SBOM ID from the path parameter
  2. Call `SbomService::advisory_severity_summary(id)` 
  3. Return `Ok(Json(summary))` on success
  4. Return the appropriate error (404) when the SBOM is not found
- Use `Result<T, AppError>` return type with `.context()` wrapping, consistent with all other handlers in the codebase.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern used for `list.rs` and `get.rs` route registration.
- Add 5-minute cache configuration using the tower-http caching middleware pattern already used in the codebase. The cache configuration should be applied at the route level in the endpoint route builder.
- The response content type should be `application/json`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- existing GET handler for SBOM details; follow the same handler structure, path extraction, and error handling pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- route registration pattern for SBOM endpoints; add the new route following the same approach
- `common/src/error.rs::AppError` -- error handling enum; reuse for 404 and 500 responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Endpoint returns 404 with appropriate error body when SBOM ID does not exist
- [ ] Response includes cache headers indicating 5-minute cache duration
- [ ] Route is registered alongside existing SBOM endpoints

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct severity counts for an SBOM with known advisories
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for a non-existent SBOM ID
- [ ] Integration test: response body contains all expected fields (critical, high, medium, low, total)
- [ ] Integration test: verify cache headers are present in the response

## Verification Commands
- `cargo test --test api -- advisory_summary` -- run integration tests for the new endpoint

## Dependencies
- Depends on: Task 1 -- Add AdvisorySeveritySummary model and service method
