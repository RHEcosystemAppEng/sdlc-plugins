## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint that exposes the SBOM comparison service (Task 2) via HTTP. This endpoint accepts two SBOM IDs as query parameters, invokes the comparison service, and returns the structured diff result. Also add integration tests that verify the endpoint against a real PostgreSQL test database.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the comparison route alongside existing SBOM routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- GET /api/v2/sbom/compare handler: parse left/right query params, call comparison service, return SbomComparisonResult as JSON
- `tests/api/sbom_compare.rs` -- integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- NEW: returns SbomComparisonResult JSON with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## Implementation Notes
- Follow the existing endpoint pattern from `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure, error handling, and route registration.
- Parse query parameters `left` and `right` using Axum's query extractor. Return 400 (Bad Request) with a descriptive error if either parameter is missing.
- Return 404 (Not Found) if either SBOM ID does not exist, using `AppError` from `common/src/error.rs`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern. The comparison route should be registered before parameterized routes (`/api/v2/sbom/{id}`) to avoid path conflicts.
- Handler signature should return `Result<Json<SbomComparisonResult>, AppError>`.
- Integration tests in `tests/api/sbom_compare.rs` should follow the pattern from `tests/api/sbom.rs`: set up test data, call the endpoint, assert response status and body shape.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- existing SBOM endpoint handler; follow its pattern for parameter extraction and error handling
- `modules/fundamental/src/sbom/endpoints/list.rs` -- existing list endpoint; reference for query parameter handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- route registration pattern to follow
- `common/src/error.rs::AppError` -- error type for handler return values
- `tests/api/sbom.rs` -- existing SBOM integration tests; follow test setup and assertion patterns

## Acceptance Criteria
- [ ] GET /api/v2/sbom/compare?left={id1}&right={id2} returns 200 with SbomComparisonResult JSON
- [ ] Missing left or right parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Response body matches the documented JSON shape with all six diff categories
- [ ] Route is registered in the SBOM endpoint module alongside existing routes

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences, verify all diff categories are populated correctly
- [ ] Integration test: compare identical SBOMs, verify empty diff (all categories empty)
- [ ] Integration test: request with missing left parameter returns 400
- [ ] Integration test: request with missing right parameter returns 400
- [ ] Integration test: request with non-existent SBOM ID returns 404
- [ ] Integration test: verify response JSON structure matches SbomComparisonResult schema

## Verification Commands
- `cargo test --test sbom_compare` -- run comparison endpoint integration tests, expect all tests to pass

## Documentation Updates
- `tests/api/sbom_compare.rs` -- new integration test file documents endpoint behavior through test cases

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 2 -- Backend: Add SBOM comparison model and diff service
