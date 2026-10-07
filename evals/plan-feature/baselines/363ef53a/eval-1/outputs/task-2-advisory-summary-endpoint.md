## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns aggregated advisory severity counts for a given SBOM (TC-9001). The endpoint delegates to `SbomService::get_advisory_summary`, returns a JSON response with severity counts, returns 404 if the SBOM ID does not exist, supports an optional `?threshold=critical|high|medium|low` query parameter, and applies a 5-minute cache using the existing tower-http caching middleware.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function for `GET /api/v2/sbom/{id}/advisory-summary` with path parameter extraction, optional threshold query parameter, 404 handling, and 5-minute cache configuration

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/advisory-summary` route and import the handler

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with optional `?threshold=critical|high|medium|low` query parameter to filter counts above a severity level

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction (`Path<Uuid>`) and 404 error handling. The existing get handler demonstrates how to extract the SBOM ID and return `AppError::NotFound` when the SBOM does not exist.
- Add the optional `threshold` query parameter using Axum's `Query<ThresholdParams>` extractor, where `ThresholdParams` is a struct with `threshold: Option<String>`.
- Apply 5-minute cache using tower-http caching middleware in the route builder, following the pattern established in existing endpoint route registrations in `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing SBOM routes. The route mounts under the existing `/api/v2/sbom` prefix.
- Per CONVENTIONS.md §Error handling: return `Result<Json<AdvisorySeveritySummary>, AppError>` with `.context()` wrapping on errors. See `modules/fundamental/src/sbom/endpoints/get.rs` for the established pattern. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` endpoint file scope.
- Per CONVENTIONS.md §Endpoint registration: register the route in `endpoints/mod.rs` following the existing route registration pattern. See `modules/fundamental/src/sbom/endpoints/mod.rs` for how existing routes are registered. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Caching: configure 5-minute cache using tower-http caching middleware in the route builder. See existing route builders in `modules/fundamental/src/sbom/endpoints/mod.rs` for cache configuration examples. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler for `/api/v2/sbom/{id}`; follow this pattern for path parameter extraction, error handling, and response structure
- `common/src/error.rs::AppError` — error enum with `IntoResponse` implementation; use for 404 and internal error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ critical: N, high: N, medium: N, low: N, total: N }`
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Optional `?threshold=critical` query parameter filters counts to only severities at or above the threshold
- [ ] Response is cached for 5 minutes via tower-http caching middleware
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`

## Test Requirements
- [ ] Handler returns 200 with correct severity counts for a valid SBOM
- [ ] Handler returns 404 for a non-existent SBOM ID
- [ ] Handler returns filtered counts when threshold query parameter is provided
- [ ] Cache headers are present in the response with 5-minute TTL

## Verification Commands
- `cargo build` — project compiles without errors
- `cargo clippy` — no lint warnings on new code

## Documentation Updates
- REST API reference — add documentation for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint including path parameters, query parameters, response shape, and example responses

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and aggregation service method
