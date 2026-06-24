# Task 3 — Backend comparison endpoint and integration tests

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Expose the SBOM comparison service via a new REST endpoint `GET /api/v2/sbom/compare?left={id}&right={id}`. Register the route in the SBOM endpoint module and add integration tests that verify the endpoint returns correct diff results with proper HTTP status codes.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route in the SBOM router, mapping to the new compare handler

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Implement the `compare` handler: extract `left` and `right` query parameters, validate both are provided, call `SbomService::compare()`, return JSON response. Return 400 if either parameter is missing, 404 if either SBOM ID is not found.
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`.
- Use Axum `Query` extractor for the `left` and `right` query parameters. Define a `CompareQuery` struct with `left: Uuid` and `right: Uuid`.
- The handler should return `Json<SbomComparison>` on success.
- For error responses, use `AppError` from `common/src/error.rs` — return `AppError::NotFound` when an SBOM ID does not exist, and `AppError::BadRequest` when query parameters are missing or malformed.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes like `list` and `get`.
- Integration tests should follow the pattern in `tests/api/sbom.rs`: set up test database with known SBOM data, call the endpoint, assert response status and body content.
- Test the p95 < 1s non-functional requirement with a test using SBOMs containing a realistic number of packages.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id}&right={id}` returns 200 with `SbomComparison` JSON
- [ ] Missing query parameters return 400 Bad Request
- [ ] Non-existent SBOM IDs return 404 Not Found
- [ ] Response JSON structure matches the schema defined in the feature requirements
- [ ] Route is registered in the SBOM endpoint module

## Test Requirements
- [ ] Integration test: valid comparison returns 200 with correct diff structure
- [ ] Integration test: missing `left` parameter returns 400
- [ ] Integration test: missing `right` parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: comparing an SBOM with itself returns empty diff categories
- [ ] Integration test: response contains correct added/removed packages for known test data

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 2 — Backend comparison model and diff service

## Digest
[sdlc-workflow] Description digest: sha256-md:2df9de0c59828c28c36fe6ce018ffd3fda64aa78f3ae5bbc09a528c2d374db7d
