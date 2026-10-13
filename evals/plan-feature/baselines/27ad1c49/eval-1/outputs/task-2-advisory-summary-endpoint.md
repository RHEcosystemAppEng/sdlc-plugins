## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST API endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns advisory severity counts for a given SBOM. The endpoint calls the `SbomService::get_advisory_summary` method created in Task 1, applies a 5-minute response cache using the existing tower-http caching middleware, and supports an optional `?threshold=critical` query parameter to filter counts above a severity level.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the advisory-summary route with 5-minute cache middleware in the SBOM router

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for GET /api/v2/sbom/{id}/advisory-summary; extracts SBOM ID from path, optional threshold from query params, calls SbomService::get_advisory_summary, applies threshold filtering, returns JSON response

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with optional `?threshold=critical|high|medium|low` query parameter to filter counts at or above the specified severity

## Implementation Notes
The handler should extract the SBOM ID from the path using Axum's `Path` extractor and the optional threshold from `Query` params. Call `SbomService::get_advisory_summary` and, if a threshold is provided, zero out counts below the threshold level before returning. The severity hierarchy is: critical > high > medium > low.

Per CONVENTIONS.md §Module pattern: place the handler in `endpoints/advisory_summary.rs`, following the `model/ + service/ + endpoints/` structure.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's module directory structure scope.

Per CONVENTIONS.md §Error handling: return `Result<Json<AdvisorySeveritySummary>, AppError>` from the handler, using `.context()` to wrap any errors from the service call.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler scope.

Per CONVENTIONS.md §Endpoint registration: register the new route in `endpoints/mod.rs`; `server/main.rs` already mounts the SBOM module.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

Per CONVENTIONS.md §Caching: configure 5-minute tower-http cache middleware on the advisory-summary route builder.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for existing SBOM endpoint handler pattern (path extraction, service call, error handling)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration pattern to follow for the new route

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body containing critical, high, medium, low, and total fields
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response is cached for 5 minutes using tower-http caching middleware
- [ ] Optional `?threshold` query parameter correctly filters severity counts
- [ ] Response Content-Type is application/json

## Test Requirements
- [ ] Integration test: GET advisory-summary returns 200 with correct severity counts for a known SBOM
- [ ] Integration test: GET advisory-summary returns 404 for non-existent SBOM ID
- [ ] Integration test: GET advisory-summary with `?threshold=high` returns only critical and high counts (medium and low zeroed)
- [ ] Integration test: verify cache headers are present in the response

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service layer
