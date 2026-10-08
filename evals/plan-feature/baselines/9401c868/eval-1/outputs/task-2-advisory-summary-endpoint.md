## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns advisory severity counts for a given SBOM. The endpoint calls the `SbomService::advisory_severity_summary` method (from Task 1), supports an optional `?threshold=critical|high|medium|low` query parameter to filter counts at or above a severity level, returns 404 when the SBOM ID does not exist, and applies a 5-minute cache TTL using the existing tower-http caching middleware. This endpoint enables dashboard widgets and alerting integrations to retrieve severity breakdowns in a single call, as specified in TC-9001.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` with optional `threshold` query parameter extraction, service call, and JSON response
- `tests/api/advisory_summary.rs` — Integration tests for the advisory summary endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/api/v2/sbom/{id}/advisory-summary` route with 5-minute cache configuration

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ critical: N, high: N, medium: N, low: N, total: N }` with optional `?threshold=critical|high|medium|low` query parameter. Returns 404 if SBOM ID does not exist. Cached for 5 minutes.

## Implementation Notes
Per CONVENTIONS.md §Module pattern: create the endpoint handler in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` following the established `model/ + service/ + endpoints/` structure. See `modules/fundamental/src/sbom/endpoints/get.rs` for the existing endpoint handler pattern.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's module directory structure scope.

Per CONVENTIONS.md §Error handling: the endpoint handler must return `Result<Json<AdvisorySeveritySummary>, AppError>` and use `.context()` wrapping. Follow the error handling pattern in `modules/fundamental/src/sbom/endpoints/get.rs`.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Endpoint registration: register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing SBOM routes. The route should be nested under the existing `/api/v2/sbom/{id}` path group. See the existing route registration pattern in `endpoints/mod.rs`.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

Per CONVENTIONS.md §Caching: apply tower-http caching middleware with a 5-minute TTL on the new route. Follow the cache configuration pattern used by existing endpoint route builders.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint `.rs` file scope.

Per CONVENTIONS.md §Testing: create integration tests in `tests/api/advisory_summary.rs` following the established pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions.
Applies: task creates `tests/api/advisory_summary.rs` matching the convention's test file scope.

The `threshold` query parameter should be parsed as an optional enum value. Invalid threshold values should return 400 Bad Request with a descriptive error message.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing `GET /api/v2/sbom/{id}` handler; follow its pattern for path parameter extraction, service injection, and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern for SBOM sub-routes
- `common/src/error.rs::AppError` — Standard error handling type
- `tests/api/sbom.rs` — Integration test patterns for SBOM endpoints; follow its test setup and assertion style

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with `critical`, `high`, `medium`, `low`, and `total` fields
- [ ] Endpoint returns 404 with appropriate error body when SBOM ID does not exist
- [ ] Endpoint supports optional `?threshold=critical` query parameter that filters counts to only severities at or above the threshold
- [ ] Endpoint returns 400 for invalid threshold values
- [ ] Response is cached for 5 minutes via tower-http caching middleware
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Integration tests pass in `tests/api/advisory_summary.rs`

## Test Requirements
- [ ] Integration test: endpoint returns correct severity counts for an SBOM with known advisories
- [ ] Integration test: endpoint returns 404 for nonexistent SBOM ID
- [ ] Integration test: endpoint returns correct filtered counts when `?threshold=high` is provided
- [ ] Integration test: endpoint returns 400 for invalid threshold value
- [ ] Integration test: endpoint returns zero counts for an SBOM with no advisories
- [ ] Integration test: verify response Content-Type is application/json

## Verification Commands
- `cargo build -p trustify-fundamental` — Compiles without errors
- `cargo test --test api -- advisory_summary` — All integration tests pass

## Documentation Updates
- REST API reference — add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with path parameters, query parameters, request/response examples, and error codes

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
