# Task 3 — Add GET /api/v2/sbom/compare endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Expose the SBOM comparison service logic as a REST endpoint at `GET /api/v2/sbom/compare?left={id1}&right={id2}`. This endpoint returns the structured diff computed by `SbomService::compare()` as a JSON response. The endpoint must validate both query parameters, return appropriate error responses for missing or invalid IDs, and meet the p95 < 1s performance requirement.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new comparison route alongside existing SBOM routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for GET /api/v2/sbom/compare
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` JSON response with structured diff between two SBOMs

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/`: each endpoint lives in its own file (`list.rs`, `get.rs`) with a handler function that uses Axum extractors and returns `Result<Json<T>, AppError>`. See `get.rs` for the established pattern.
- Register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern.
- Use Axum `Query` extractor to parse `left` and `right` query parameters as UUID types.
- Return 400 Bad Request if either query parameter is missing or not a valid UUID.
- Return 404 Not Found if either SBOM ID does not exist (propagated from `SbomService::compare()`).
- The handler should call `SbomService::compare(left, right)` and return the result as `Json<SbomComparisonResult>`.
- Integration tests should follow the pattern in `tests/api/sbom.rs` — hit a real PostgreSQL test database, assert on `resp.status()` and response body structure.
- Add the comparison test file to `tests/api/` and ensure it is included in the test module.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM endpoint handler demonstrating the Axum handler pattern, error handling, and service injection
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for SBOM endpoints
- `common/src/error.rs::AppError` — error type that implements IntoResponse for consistent HTTP error responses
- `tests/api/sbom.rs` — existing SBOM integration tests demonstrating test setup, database fixtures, and assertion patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with structured diff JSON
- [ ] Missing query parameters return 400 Bad Request
- [ ] Non-existent SBOM IDs return 404 Not Found
- [ ] Response shape matches the documented contract (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] Endpoint is registered and accessible via the server route tree

## Test Requirements
- [ ] Integration test: successful comparison returns 200 with correct diff structure
- [ ] Integration test: missing `left` parameter returns 400
- [ ] Integration test: missing `right` parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: both SBOMs identical returns 200 with empty diff sections

## Verification Commands
- `cargo test --package trustify-tests -- api::sbom_compare` — all integration tests pass
- `cargo check --workspace` — no compilation errors across workspace

## Documentation Updates
- `README.md` — add the comparison endpoint to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison diff model and service logic
