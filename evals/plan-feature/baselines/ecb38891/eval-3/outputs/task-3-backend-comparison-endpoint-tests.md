## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` REST endpoint that accepts `left` and `right` query parameters (SBOM IDs), calls the `SbomService::compare` method (from Task 2), and returns the structured diff as JSON. Also add integration tests covering the endpoint behavior.

The endpoint enables the frontend comparison page and API consumers to retrieve a structured diff between two SBOM versions.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the comparison route alongside existing SBOM routes (`/api/v2/sbom/compare`)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — endpoint handler for `GET /api/v2/sbom/compare`
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` JSON with six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
- Follow the existing endpoint pattern established by `modules/fundamental/src/sbom/endpoints/get.rs` and `list.rs`:
  - The handler function should accept `Query<CompareParams>` (Axum extractor) for the `left` and `right` query parameters
  - Return `Result<Json<SbomComparisonResult>, AppError>` consistent with other handlers
  - Call `SbomService::compare(left, right)` from the service layer (Task 2)
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes. The route must be registered BEFORE the `/{id}` route to avoid path conflicts (Axum matches routes in order — `/compare` must not be captured as an `{id}` parameter).
- Validate that both `left` and `right` query parameters are present; return 400 Bad Request if either is missing.
- For integration tests, follow the pattern in `tests/api/sbom.rs`:
  - Use a real PostgreSQL test database
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern
  - Set up test data by ingesting two SBOMs with known package differences
- Consider adding the endpoint to `tower-http` caching configuration if appropriate (comparison results are deterministic for the same inputs).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for endpoint handler pattern (Axum extractors, error handling, response type)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `tests/api/sbom.rs` — reference for integration test setup, assertions, and test database patterns
- `common/src/error.rs::AppError` — error type with IntoResponse implementation for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON body
- [ ] Missing `left` or `right` parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Response Content-Type is `application/json`
- [ ] Endpoint is accessible at the correct path under `/api/v2/sbom/compare`
- [ ] Route does not conflict with existing `/api/v2/sbom/{id}` route
- [ ] Endpoint response time is p95 < 1s for SBOMs with up to 2000 packages each
- [ ] Integration tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Integration test: GET with valid left and right SBOM IDs returns 200 with correct diff structure
- [ ] Integration test: GET with missing left parameter returns 400
- [ ] Integration test: GET with missing right parameter returns 400
- [ ] Integration test: GET with non-existent SBOM ID returns 404
- [ ] Integration test: GET with identical left and right SBOM IDs returns 200 with empty diff categories
- [ ] Integration test: response body deserializes correctly into `SbomComparisonResult`

## Verification Commands
- `cargo test --test sbom_compare` — run comparison endpoint integration tests
- `cargo clippy --all-targets` — verify no lint warnings

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Backend comparison model and service logic
