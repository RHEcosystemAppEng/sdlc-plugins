## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that calls the service layer to retrieve aggregated severity counts. This endpoint supports an optional `?threshold` query parameter to filter counts above a specified severity level. The handler follows the existing Axum endpoint patterns established in the sbom module.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Endpoint handler for GET /api/v2/sbom/{id}/advisory-summary

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new advisory-summary route alongside existing sbom routes

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns aggregated advisory severity counts `{ critical, high, medium, low, total }` for the given SBOM
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: Filters to return only counts at or above the specified severity threshold

## Implementation Notes
Create the endpoint handler in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` following the pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}).

The handler should:
1. Extract the SBOM `id` from the path using Axum's `Path` extractor
2. Extract the optional `threshold` query param using Axum's `Query` extractor with `Option<SeverityThreshold>`
3. Call `SbomService::get_advisory_severity_summary(id)` from the service layer
4. If `threshold` is provided, zero out severity counts below the threshold before returning
5. Return the `AdvisorySeveritySummary` as a JSON response with `axum::Json`

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` by adding a `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::handler))` call to the existing router, following the same registration pattern used for `list.rs` and `get.rs`.

Per CONVENTIONS.md §Error Handling: use Result<T, AppError> with .context() wrapping.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Follow the same handler signature, path extraction, and error handling pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow
- `common/src/error.rs::AppError` — Error type for the handler return type

## Acceptance Criteria
- [ ] GET /api/v2/sbom/{id}/advisory-summary returns JSON with fields: critical, high, medium, low, total
- [ ] Endpoint returns 404 with appropriate error when SBOM ID does not exist
- [ ] Optional ?threshold query param filters severity counts (zeroes out levels below threshold)
- [ ] Route is registered in sbom endpoints/mod.rs
- [ ] Handler returns Result<Json<AdvisorySeveritySummary>, AppError>

## Test Requirements
- [ ] Handler unit test verifying JSON response shape for a valid SBOM
- [ ] Handler unit test verifying 404 response for non-existent SBOM ID

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

## Dependencies
- Depends on: Task 1 — Advisory severity summary model
- Depends on: Task 2 — Severity aggregation service

[sdlc-workflow] Description digest: sha256-md:c6e9f1b3d5a7280795a31c6d7f0b4d8e9c12e3f5a7b9201c3d5e7f9a1b2c4d6
