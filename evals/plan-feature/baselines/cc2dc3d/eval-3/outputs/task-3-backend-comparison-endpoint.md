## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare?left={id1}&right={id2}` HTTP endpoint that exposes the SBOM comparison service to the API. The endpoint accepts two SBOM IDs as query parameters, delegates to `SbomService::compare_sboms`, and returns the structured diff as JSON.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for the comparison endpoint with query parameter extraction

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/compare` route alongside existing SBOM routes
- `tests/api/sbom.rs` — add integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` JSON with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/` — see `list.rs` (GET /api/v2/sbom) and `get.rs` (GET /api/v2/sbom/{id}) for the handler function structure.
- Define a `CompareQuery` struct with `left: String` and `right: String` fields, deriving `Deserialize` for Axum query parameter extraction (use `axum::extract::Query<CompareQuery>`).
- The handler should:
  1. Extract the `left` and `right` query parameters
  2. Validate both IDs are present (return 400 Bad Request if missing)
  3. Call `SbomService::compare_sboms(left, right)`
  4. Return the result as `Json<SbomComparisonResult>` with 200 OK
  5. Handle errors: return 404 if either SBOM ID is not found, 500 for internal errors
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern used for `list.rs` and `get.rs`.
- Mount the route at `/api/v2/sbom/compare` — ensure it is registered before the `/{id}` route to avoid path conflicts.
- The p95 response time requirement is <1s for SBOMs with up to 2000 packages each. Consider the query efficiency of the comparison service, but do not add caching in this task.

**Reuse Candidates:**
- `modules/fundamental/src/sbom/endpoints/get.rs` — follow the same handler function structure and error handling pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — follow the route registration pattern
- `common/src/error.rs::AppError` — reuse for error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with the structured comparison JSON
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Route is properly registered alongside existing SBOM endpoints
- [ ] Response JSON shape matches the expected contract (six diff category arrays)

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences, verify response structure and content
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: comparing an SBOM with itself returns empty diff arrays
- [ ] Follow the existing test pattern in `tests/api/sbom.rs` using `assert_eq!(resp.status(), StatusCode::OK)`

## Verification Commands
- `cargo test --test api sbom::compare` — expected: all comparison endpoint tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model and service
