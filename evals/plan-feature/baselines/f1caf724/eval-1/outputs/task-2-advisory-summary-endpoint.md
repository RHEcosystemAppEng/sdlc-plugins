## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns advisory severity counts for a given SBOM. The endpoint calls the `SbomService::get_advisory_severity_summary` method (from Task 1), applies 5-minute response caching using the existing `tower-http` caching middleware, and supports an optional `?threshold=critical` query parameter to filter counts above a severity level. Returns 404 if the SBOM ID does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for the advisory-summary endpoint

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with optional `?threshold=critical|high|medium|low` query parameter

## Implementation Notes
- Per CONVENTIONS.md §Endpoint Registration: register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the established pattern used by `list.rs` and `get.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Error Handling: the handler must return `Result<Json<SeveritySummary>, AppError>` and wrap service errors with `.context()`.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler scope.
- Per CONVENTIONS.md §Caching: configure `tower-http` caching middleware with a 5-minute TTL on the route builder, consistent with how other cached endpoints are configured.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint scope.
- Parse the `id` path parameter as a UUID and the optional `threshold` query parameter as a severity enum value.
- Reference `modules/fundamental/src/sbom/endpoints/get.rs` for the existing pattern of extracting SBOM ID from path parameters and returning structured responses.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET handler; follow its pattern for path parameter extraction and error handling
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing SBOM list handler; reference for route registration pattern
- `common/src/error.rs::AppError` — error enum for 404 and 500 responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` JSON response
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response is cached for 5 minutes via `tower-http` caching middleware
- [ ] Optional `?threshold` query parameter filters counts to only include severities at or above the specified level
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`

## Test Requirements
- [ ] Handler returns correct JSON structure with severity counts
- [ ] Handler returns 404 for non-existent SBOM ID
- [ ] Cache headers indicate 5-minute cache duration
- [ ] Threshold query parameter produces filtered response

## Verification Commands
- `cargo check --package trustify-fundamental` — verify compilation
- `cargo test --package trustify-fundamental -- sbom::endpoints::tests::advisory_summary` — verify handler tests pass

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service method
