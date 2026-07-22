## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` HTTP endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint includes 5-minute response caching and an optional `?threshold` query parameter for filtering counts above a specified severity level. This is the primary endpoint that frontend dashboard widgets and alerting integrations will consume.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new advisory-summary route under `/api/v2/sbom/{id}/advisory-summary`

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Handler function for the advisory-summary endpoint

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ critical: N, high: N, medium: N, low: N, total: N }` with optional `?threshold=critical|high|medium|low` query param

## Implementation Notes
Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs`. Define an async handler function that extracts the SBOM ID from the path and an optional `threshold` query parameter. Call `SbomService::advisory_summary` from `modules/fundamental/src/sbom/service/sbom.rs`. Return `Result<Json<AdvisorySeveritySummary>, AppError>` using the error handling convention from `common/src/error.rs`. Configure 5-minute caching using `tower-http` caching middleware on the route builder, consistent with the caching convention described in Key Conventions. Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for existing routes like `get.rs` and `list.rs`. When `threshold` is provided, filter the response to include only severity levels at or above the specified threshold and recalculate total accordingly.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Pattern for SBOM endpoint handler with path extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern
- `common/src/error.rs::AppError` — Error type implementing IntoResponse for consistent error handling

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with critical, high, medium, low, total fields
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response is cached for 5 minutes
- [ ] Optional `?threshold` query parameter filters severity counts
- [ ] Route is registered and accessible through the server

## Test Requirements
- [ ] Handler returns 200 with correct JSON shape for valid SBOM
- [ ] Handler returns 404 for nonexistent SBOM ID
- [ ] Cache headers indicate 5-minute caching
- [ ] Threshold parameter filters response correctly

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental` — all tests pass

## Dependencies
- Depends on: Task 2 — Implement advisory severity aggregation service