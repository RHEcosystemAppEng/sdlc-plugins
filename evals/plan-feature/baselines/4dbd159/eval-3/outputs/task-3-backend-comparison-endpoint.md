# Task 3 — Add SBOM comparison endpoint and integration tests

## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint handler that accepts two SBOM IDs as query parameters, calls the comparison service method, and returns the structured diff as JSON. Register the route in the SBOM endpoints module and add integration tests.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Endpoint handler for `GET /api/v2/sbom/compare`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route and add `pub mod compare;`
- `tests/api/sbom.rs` — Add integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` JSON with 200 OK. Returns 404 if either SBOM ID does not exist. Returns 400 if query parameters are missing.

## Implementation Notes
- Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`:
  - Handlers are async functions taking Axum extractors
  - Return `Result<Json<T>, AppError>` where `T` is the response type
  - Use `Query` extractor for query parameters
- Define a `CompareParams` struct with `left` and `right` fields (both SBOM ID types) deriving `Deserialize` for the Axum `Query` extractor.
- Route registration follows the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — add `.route("/compare", get(compare::handler))` to the existing router builder.
- The handler should:
  1. Extract `left` and `right` from query parameters
  2. Call `SbomService::compare(left, right)` 
  3. Return `Json(result)` on success
- Integration tests in `tests/api/sbom.rs` should follow the existing pattern: hit a real PostgreSQL test database and assert `resp.status() == StatusCode::OK`.
- Test both success and error cases (missing params → 400, invalid IDs → 404).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Follow the handler function signature and error handling pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — Follow the route registration pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route mounting pattern for adding new routes
- `common/src/error.rs::AppError` — Error type for 400/404 responses
- `tests/api/sbom.rs` — Follow existing integration test patterns and test database setup

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Missing query parameters return 400 Bad Request
- [ ] Non-existent SBOM IDs return 404 Not Found
- [ ] Route is registered in the SBOM endpoints module
- [ ] Integration tests pass against a test database

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences, assert response contains expected diff categories
- [ ] Integration test: request with missing `left` parameter returns 400
- [ ] Integration test: request with missing `right` parameter returns 400
- [ ] Integration test: request with non-existent SBOM ID returns 404
- [ ] Integration test: compare two identical SBOMs returns empty diff categories

## Verification Commands
- `cargo build -p trustify-server` — full server compiles with new route
- `cargo test -p trustify-tests sbom` — integration tests pass

## Documentation Updates
- `README.md` — Add the comparison endpoint to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 2 — Add SBOM comparison service logic
