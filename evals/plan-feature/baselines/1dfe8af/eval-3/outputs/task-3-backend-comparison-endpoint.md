## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Expose the SBOM comparison service as a REST endpoint at `GET /api/v2/sbom/compare` with query parameters `left` and `right` for the two SBOM IDs. Register the endpoint in the SBOM module's route configuration and add integration tests.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- Handler for `GET /api/v2/sbom/compare?left={id1}&right={id2}`
- `tests/api/sbom_compare.rs` -- Integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Add `pub mod compare;` and register the comparison route alongside existing SBOM routes
- `tests/api/mod.rs` -- Add `mod sbom_compare;` to include comparison tests (if a mod.rs exists; otherwise the test runner auto-discovers)

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- NEW: Returns an `SbomComparison` JSON response with six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`. The handler should:

1. Parse `left` and `right` query parameters as SBOM IDs (return 400 if missing or invalid)
2. Call `SbomService::compare(left, right)` from the new comparison service in `modules/fundamental/src/sbom/service/compare.rs`
3. Return 404 if either SBOM ID is not found (the service should propagate this via `AppError`)
4. Return the `SbomComparison` struct as JSON with 200 status

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern used for the existing `list` and `get` routes. The route should be mounted at `/api/v2/sbom/compare` in the SBOM module's router.

Integration tests should follow the pattern in `tests/api/sbom.rs`, using the real PostgreSQL test database and the `assert_eq!(resp.status(), StatusCode::OK)` convention.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- Pattern reference for single-resource endpoint handler
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Route registration pattern to follow
- `common/src/error.rs::AppError` -- Error handling with proper HTTP status code mapping
- `tests/api/sbom.rs` -- Integration test patterns for SBOM endpoints

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with valid `SbomComparison` JSON
- [ ] Missing `left` or `right` parameter returns 400
- [ ] Non-existent SBOM ID returns 404
- [ ] Response JSON shape matches the contract defined in feature requirements
- [ ] Endpoint appears in OpenAPI spec via utoipa annotations

## Test Requirements
- [ ] Integration test: valid comparison returns 200 with correct diff structure
- [ ] Integration test: missing query parameters returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: comparing an SBOM with itself returns empty diff categories

## Dependencies
- Depends on: Task 2 -- Implement SBOM comparison model and service

[sdlc-workflow] Description digest: sha256-md:c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5
