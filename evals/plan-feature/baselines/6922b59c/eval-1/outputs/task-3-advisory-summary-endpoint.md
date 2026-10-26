## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns advisory severity counts for a given SBOM. The endpoint handler calls `SbomService::advisory_severity_summary` and returns the `AdvisorySeveritySummary` as JSON. The response is cached for 5 minutes using `tower-http` caching middleware. An optional `?threshold=<severity>` query parameter filters the response to include only counts at or above the specified severity level (non-MVP requirement, useful for alerting integrations).

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler function `get_advisory_summary` accepting SBOM ID path param and optional `threshold` query param

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route with 5-minute cache configuration

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with `Content-Type: application/json`
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: filters counts to only include severity levels at or above the specified threshold

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure, extractor usage (`Path<Uuid>` for the SBOM ID, `Query<ThresholdParams>` for the optional threshold parameter), and error propagation.

For the `threshold` query parameter, define a `ThresholdParams` struct with `threshold: Option<String>`. Validate that the value is one of `critical`, `high`, `medium`, `low` (case-insensitive). If an invalid value is provided, return a 400 Bad Request. The threshold filter should zero out counts below the specified severity level in the response.

For caching, configure the route with a 5-minute TTL using the same `tower-http` caching middleware pattern used by other endpoints in `endpoints/mod.rs`. Set `Cache-Control: public, max-age=300` on the response.

Per CONVENTIONS.md §Endpoint Registration: register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` and ensure it is mounted by the existing route builder.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

Per CONVENTIONS.md §Error Handling: handler returns `Result<Json<AdvisorySeveritySummary>, AppError>` with `.context()` wrapping on service calls.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Caching: configure cache TTL in the route builder using `tower-http` caching middleware.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET handler demonstrating the extractor pattern, error handling, and response structure to follow
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration and caching middleware configuration patterns
- `common/src/error.rs::AppError` — error type and `IntoResponse` implementation for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Response includes `Cache-Control: public, max-age=300` header for 5-minute caching
- [ ] Optional `?threshold=<severity>` query parameter filters counts to severity levels at or above the threshold
- [ ] Invalid threshold values return 400 Bad Request
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`

## Test Requirements
- [ ] Integration test: successful 200 response with valid SBOM ID
- [ ] Integration test: 404 response for non-existent SBOM ID
- [ ] Integration test: cache headers present on response
- [ ] Integration test: threshold query param returns filtered counts
- [ ] Integration test: invalid threshold value returns 400

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental advisory_summary` — endpoint tests pass
- `curl -s http://localhost:8080/api/v2/sbom/{id}/advisory-summary | jq .` — returns expected JSON shape

## Dependencies
- Depends on: Task 1 — Add advisory severity summary response model
- Depends on: Task 2 — Add SBOM advisory severity aggregation service method
