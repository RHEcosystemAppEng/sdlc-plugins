## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs), invokes the comparison service, and returns the structured diff response. Register the route in the SBOM module's endpoint configuration and add integration tests.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/compare` route in the SBOM endpoint router

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for `GET /api/v2/sbom/compare`
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: accepts two SBOM IDs as query parameters, returns `SbomComparisonResult` as JSON

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `list.rs`:
  - Extract query parameters using Axum's `Query` extractor for `left` and `right` SBOM IDs.
  - Call `SbomService::compare(left_id, right_id)` and return the result as JSON.
  - Return `Result<Json<SbomComparisonResult>, AppError>` to follow the error handling convention.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes, using `.route("/compare", get(compare_handler))`.
- Validate that both `left` and `right` query parameters are present — return a 400 Bad Request if either is missing.
- Integration tests should follow the pattern in `tests/api/sbom.rs`:
  - Test successful comparison of two SBOMs with known differences.
  - Test comparison with identical SBOMs (empty diff).
  - Test with missing query parameter (expect 400).
  - Test with non-existent SBOM ID (expect 404).
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing handler demonstrating Axum extractor patterns and error handling
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing handler showing query parameter extraction
- `tests/api/sbom.rs` — existing integration test file demonstrating test setup and assertion patterns
- `common/src/error.rs::AppError` — error type for handler return values

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Missing `left` or `right` query parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Route is registered in the SBOM endpoint module
- [ ] Response content type is `application/json`

## Test Requirements
- [ ] Integration test: compare two SBOMs with a known added package — verify `added_packages` in response
- [ ] Integration test: compare two identical SBOMs — verify all diff arrays are empty
- [ ] Integration test: missing `right` query param — verify 400 response
- [ ] Integration test: non-existent SBOM ID — verify 404 response

## Verification Commands
- `cargo test --test api sbom_compare` — run comparison endpoint integration tests
- `curl "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>"` — manually verify endpoint response

## Documentation Updates
- `README.md` — add the comparison endpoint to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison service logic

## Description Digest
sha256-md:200aac2f048693fb65e35368022179082cfaec9dd72398274a3683ba117e5f0d
