## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the REST endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that exposes the SBOM comparison service. The endpoint accepts two SBOM IDs as query parameters, invokes the comparison service, and returns the structured diff result. Also add integration tests that validate the endpoint against a real PostgreSQL test database.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- Handler for GET /api/v2/sbom/compare with query parameter extraction and response serialization

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Register the /compare route in the SBOM endpoint router
- `tests/api/sbom.rs` -- Add integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- NEW: Returns a structured diff between two SBOMs as JSON. Query parameters `left` and `right` are required SBOM UUIDs. Returns 200 with SbomComparisonResult body, 400 if either parameter is missing, 404 if either SBOM ID is not found.

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure: extract query params, call service, return JSON response.
- Define a query parameter struct (e.g., `CompareParams { left: Uuid, right: Uuid }`) and use Axum's `Query` extractor.
- Return errors as `AppError` for missing/invalid parameters (400) and non-existent SBOMs (404), following the error pattern in `common/src/error.rs`.
- Register the route in `endpoints/mod.rs` alongside existing list and get routes. The route pattern is `/compare` under the `/api/v2/sbom` prefix.
- Integration tests should follow the pattern in `tests/api/sbom.rs`: set up test data, call the endpoint, assert response status and body structure.
- Per CONVENTIONS.md: register the route in `endpoints/mod.rs` following the existing route registration pattern.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md: integration tests should use `assert_eq!(resp.status(), StatusCode::OK)` pattern and hit a real PostgreSQL test database.
  Applies: task modifies `tests/api/sbom.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- GET /api/v2/sbom/{id} handler; follow the same Axum handler pattern for query extraction and JSON response
- `modules/fundamental/src/sbom/endpoints/list.rs` -- GET /api/v2/sbom handler; reference for route registration pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Route registration module; add new route here
- `common/src/error.rs::AppError` -- Error type for 400/404 responses
- `tests/api/sbom.rs` -- Existing SBOM integration tests; follow the test setup and assertion patterns

## Acceptance Criteria
- [ ] GET /api/v2/sbom/compare?left={id1}&right={id2} returns 200 with SbomComparisonResult JSON body
- [ ] Returns 400 when left or right query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist in the database
- [ ] Response body matches the documented API contract shape with all six diff categories
- [ ] Endpoint is registered under /api/v2/sbom/compare in the route tree

## Test Requirements
- [ ] Integration test: compare two valid SBOMs returns 200 with correct diff structure
- [ ] Integration test: missing left parameter returns 400
- [ ] Integration test: missing right parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: comparing SBOM with itself returns 200 with empty diff categories

## Verification Commands
- `cargo test --test sbom` -- Expected: all SBOM integration tests pass including new comparison tests
- `cargo build` -- Expected: project compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 2 -- Implement SBOM comparison diff model and service
