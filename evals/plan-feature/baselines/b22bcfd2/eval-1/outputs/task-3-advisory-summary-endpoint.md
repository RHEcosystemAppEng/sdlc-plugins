## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns aggregated advisory severity counts for a given SBOM. This endpoint calls `SbomService::get_advisory_severity_summary` and returns the result as JSON. It also adds 5-minute cache-control headers using the existing `tower-http` caching middleware, and supports an optional `?threshold` query parameter to filter counts above a specified severity level.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for GET /api/v2/sbom/{id}/advisory-summary

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the advisory-summary route alongside existing SBOM routes
- `server/src/main.rs` — ensure the SBOM module routes (which now include advisory-summary) are mounted (likely already handled by existing module registration)

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 5-minute cache TTL
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: filters to return only counts at or above the specified severity level

## Implementation Notes
Create the endpoint handler in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` following the pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}):

1. Define an async handler function that extracts `Path(id)` and optional `Query(params)` with a `threshold` field
2. Call `SbomService::get_advisory_severity_summary(id)` — the service already handles 404 for missing SBOMs
3. If `threshold` query param is present, filter the response to include only severity levels at or above the threshold (e.g., `threshold=high` returns critical + high counts only, with medium and low set to 0)
4. Return `Json(summary)` with `Result<Json<AdvisorySeveritySummary>, AppError>` return type

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern. Add the route as `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary))`.

For caching, apply `tower-http` cache-control middleware to the route with a 5-minute max-age, following the cache configuration pattern documented in the repo's key conventions (endpoint route builders).

The handler return type should follow the `Result<T, AppError>` pattern from `common/src/error.rs`, consistent with all other handlers.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — pattern for SBOM endpoint handler with Path extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — error handling for endpoint responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ critical, high, medium, low, total }`
- [ ] Returns 404 when SBOM ID does not exist
- [ ] Response includes cache-control header with 5-minute max-age
- [ ] Optional `?threshold` query parameter filters counts to only severity levels at or above the threshold
- [ ] Route is registered in the SBOM endpoints module

## Test Requirements
- [ ] Handler unit test verifying 200 response with correct JSON shape
- [ ] Handler unit test verifying 404 for non-existent SBOM
- [ ] Handler unit test verifying threshold filtering (e.g., threshold=high returns critical+high only)
- [ ] Verify cache-control header is present with 300-second max-age

## Dependencies
- Depends on: Task 2 — Add severity aggregation query to SbomService

## additional_fields
- priority: Major
- fixVersions: RHTPA 1.5.0