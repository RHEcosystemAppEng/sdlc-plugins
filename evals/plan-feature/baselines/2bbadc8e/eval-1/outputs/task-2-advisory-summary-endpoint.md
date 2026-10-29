## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns advisory severity counts for a given SBOM. The endpoint uses the `SbomService::advisory_summary` method (from Task 1) and includes 5-minute response caching via tower-http middleware. It supports an optional `?threshold` query parameter to filter counts to severity levels at or above a specified threshold. The endpoint returns 404 for non-existent SBOM IDs, consistent with existing SBOM endpoints.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new advisory-summary route in the SBOM endpoint group

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for GET /api/v2/sbom/{id}/advisory-summary
- `tests/api/advisory_summary.rs` — integration tests for the new endpoint

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with 5-minute cache
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={level}` — NEW: optional query parameter; valid values: `critical`, `high`, `medium`, `low`; filters counts to severity levels at or above the threshold

## Implementation Notes
- Follow the endpoint handler pattern from the existing `get.rs` handler (`modules/fundamental/src/sbom/endpoints/get.rs`) which handles `GET /api/v2/sbom/{id}`.
- Register the route in `endpoints/mod.rs` following the existing route registration pattern — add `.route("/api/v2/sbom/{id}/advisory-summary", get(advisory_summary))` alongside existing SBOM routes.
- Configure tower-http cache middleware with `max-age=300` (5 minutes) on the route builder, following the caching pattern documented in the repository's conventions.
- The handler extracts the SBOM `{id}` path parameter, calls `SbomService::advisory_summary`, and returns the result as JSON.
- For the `?threshold` query parameter: define a `ThresholdQuery` struct with `threshold: Option<String>`, validate against allowed values (`critical`, `high`, `medium`, `low`), and filter the response fields. Severity ordering: Critical > High > Medium > Low. When threshold is `high`, return critical + high counts; when threshold is `critical`, return only critical count. Always include `total` reflecting the filtered sum.
- Return 404 via `AppError` (`common/src/error.rs`) when the SBOM does not exist — this is handled by the service method from Task 1.
- Return 400 for invalid threshold values with a descriptive error message.
- Per CONVENTIONS.md §Endpoint Registration: register routes in `endpoints/mod.rs`; `server/src/main.rs` mounts all modules. See existing route registration in `modules/fundamental/src/sbom/endpoints/mod.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's .rs endpoint registration scope.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` with `.context()` wrapping. See `common/src/error.rs` for the `AppError` enum and `IntoResponse` implementation.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's .rs handler scope.
- Per CONVENTIONS.md §Caching: use tower-http caching middleware with cache configuration in endpoint route builders.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's .rs endpoint scope.
- Per CONVENTIONS.md §Testing: integration tests go in `tests/api/` and hit a real PostgreSQL test database using the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/advisory_summary.rs` matching the convention's .rs test file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET /api/v2/sbom/{id} handler; follow the same pattern for path parameter extraction, service invocation, and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — error type for 404 and 400 responses
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow the same test setup and assertion patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body containing `critical`, `high`, `medium`, `low`, `total` fields
- [ ] Endpoint returns 404 with appropriate error body when SBOM ID does not exist
- [ ] Response includes `Cache-Control` header with `max-age=300` (5-minute cache)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count and adjusted total
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts and adjusted total
- [ ] Endpoint returns 400 for invalid threshold values (e.g., `?threshold=unknown`)

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct severity counts for a SBOM with known advisories
- [ ] Integration test: `GET /api/v2/sbom/{nonexistent}/advisory-summary` returns 404
- [ ] Integration test: response includes `Cache-Control` header with `max-age=300`
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns filtered counts
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400

## Verification Commands
- `cargo build -p trustify-fundamental` — compiles without errors
- `cargo test --test advisory_summary` — integration tests pass

## Documentation Updates
- API documentation — add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint with path, method, parameters, response shape, and cache behavior

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
