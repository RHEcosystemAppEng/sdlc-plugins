# Task 4 — Add SBOM comparison endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Wire the SBOM comparison service logic to a new HTTP endpoint at `GET /api/v2/sbom/compare?left={id1}&right={id2}`. This endpoint accepts two SBOM IDs as query parameters, calls the `SbomService::compare` method, and returns the structured diff as JSON. The endpoint must validate that both query parameters are present and return appropriate error responses for missing or invalid parameters.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `compare` route alongside existing SBOM routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for `GET /api/v2/sbom/compare`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` JSON response with fields `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` — define a handler function that extracts query parameters, calls the service, and returns the result.
- Per the backend key conventions (Endpoint registration): each module's `endpoints/mod.rs` registers routes. Add the compare route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs`.
- Per the backend key conventions (Error handling): return `Result<Json<SbomComparisonResult>, AppError>` from the handler. Use `.context()` wrapping for error propagation.
- Define a query parameter struct (e.g., `CompareQuery { left: String, right: String }`) using Axum's `Query` extractor. Return HTTP 400 if either parameter is missing.
- Per the non-functional requirements: the endpoint should respond within p95 < 1s for SBOMs with up to 2000 packages each. No additional caching is needed for the initial implementation, but consider `tower-http` caching middleware configuration if needed in the future.
- Per constraint 2.1/2.2/2.3: commit message must reference TC-9003, follow Conventional Commits, and include the AI attribution trailer.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for handler function structure, error handling, and Axum extractor usage
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for route registration pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route mounting pattern
- `common/src/error.rs::AppError` — the error enum for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Missing `left` or `right` query parameter returns HTTP 400 with an error message
- [ ] Non-existent SBOM ID returns an appropriate HTTP error (404)
- [ ] The route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with correct diff structure
- [ ] Integration test: missing query parameters return 400
- [ ] Integration test: non-existent SBOM IDs return appropriate error status
- [ ] Follow the test pattern in `tests/api/sbom.rs` — use `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Verification Commands
- `cargo test --package trustify-tests -- api::sbom::compare` — run comparison endpoint integration tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison service logic
