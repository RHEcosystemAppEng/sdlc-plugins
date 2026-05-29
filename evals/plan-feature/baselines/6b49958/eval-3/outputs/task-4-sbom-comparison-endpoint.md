## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the REST endpoint `GET /api/v2/sbom/compare` that accepts two SBOM IDs as query parameters (`left` and `right`) and returns the structured comparison result computed by the service layer added in Task 3. This endpoint enables the frontend to request SBOM diffs.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new comparison route alongside existing SBOM routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — implement the comparison endpoint handler with query parameter extraction and response serialization
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: accepts two SBOM ID query parameters, returns `SbomComparisonResult` JSON with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes arrays

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/get.rs`: extract query parameters, call the service method, return JSON response.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` using the same pattern as existing routes (e.g., `.route("/api/v2/sbom/compare", get(compare))`). Register it before the `/{id}` route to avoid path conflicts.
- The handler should extract `left` and `right` as query parameters using Axum's `Query` extractor with a `CompareQuery` struct.
- Return 400 Bad Request if either `left` or `right` parameter is missing.
- Return 404 Not Found if either SBOM ID does not exist (propagated from `SbomService::compare`).
- The handler returns `Result<Json<SbomComparisonResult>, AppError>` following the standard error handling pattern from `common/src/error.rs`.
- Integration tests should follow the pattern in `tests/api/sbom.rs`: set up test data, call the endpoint, assert status code and response shape.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference pattern for single-resource endpoint handler with Axum extractors
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference pattern for query parameter extraction
- `common/src/db/query.rs` — shared query builder helpers if needed for filtering
- `tests/api/sbom.rs` — established integration test patterns for SBOM endpoints

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Missing `left` or `right` query parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Response shape matches the contract: `{ added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes }`
- [ ] Route is registered and accessible at `/api/v2/sbom/compare`

## Test Requirements
- [ ] Integration test: valid comparison request returns 200 with correct diff structure
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: comparing identical SBOMs returns 200 with all empty arrays
- [ ] Integration test: response includes correct counts for added/removed packages with known test data

## Documentation Updates
- `README.md` — add the new comparison endpoint to the API endpoint listing

## Dependencies
- Depends on: Task 3 — Add SBOM comparison diff model and service

[sdlc-workflow] Description digest: sha256:546be501e0201d3a81594fb2081e9cb8d073f67a342216f57589e9305dbec984
