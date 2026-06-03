# Task 4 — Add GET /api/v2/sbom/compare endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the REST endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that returns a structured diff between two SBOMs. The endpoint accepts two SBOM IDs as query parameters, delegates to the `SbomComparisonService`, and returns the `SbomComparisonResult` as JSON. This is the backend API that the frontend comparison page will call.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for `GET /api/v2/sbom/compare` that extracts `left` and `right` query params and calls `SbomComparisonService::compare()`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/compare` route in the SBOM endpoint router
- `server/src/main.rs` — Ensure the SBOM module routes (which already include this module's endpoints) are mounted (likely no change needed, but verify)

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` JSON with six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` for handler function structure, query parameter extraction, and error response handling.
- Use Axum's `Query` extractor for the `left` and `right` query parameters. Define a `CompareQuery` struct with `left: String` and `right: String` fields.
- Return `Result<Json<SbomComparisonResult>, AppError>` matching the pattern in existing handlers.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern as `list.rs` and `get.rs` route registration.
- The route must be registered before the `/{id}` route to avoid path parameter conflicts (Axum matches routes in order; `/compare` would be captured as an `{id}` if registered after).
- Validate that both `left` and `right` parameters are provided; return 400 Bad Request if either is missing.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing GET handler pattern for SBOM endpoints
- `modules/fundamental/src/sbom/endpoints/list.rs` — Existing list handler with query parameter extraction pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow
- `common/src/error.rs::AppError` — Error type with IntoResponse for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a valid `SbomComparisonResult` JSON body
- [ ] Returns 400 when either `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response JSON matches the expected shape with snake_case field names
- [ ] Route is correctly registered in the SBOM endpoint module

## Test Requirements
- [ ] Integration test: call `/api/v2/sbom/compare` with two valid SBOM IDs — verify 200 response with correct diff structure
- [ ] Integration test: call with missing `left` parameter — verify 400 response
- [ ] Integration test: call with missing `right` parameter — verify 400 response
- [ ] Integration test: call with non-existent SBOM ID — verify 404 response
- [ ] Integration test: call with identical SBOM IDs — verify 200 with empty diff categories

## Verification Commands
- `cargo test --test api sbom_compare` — expected: all comparison endpoint integration tests pass
- `cargo build` — expected: no compilation errors

## Documentation Updates
- `README.md` — Add the new comparison endpoint to the API endpoint list if one exists

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison diff model structs
- Depends on: Task 3 — Add SBOM comparison service logic
