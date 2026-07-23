## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare?left={id1}&right={id2}` REST endpoint that exposes the SBOM comparison service created in Task 2. This endpoint accepts two SBOM IDs as query parameters, validates them, invokes the comparison service, and returns the structured diff result. Register the route in the SBOM endpoints module and add integration tests.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- handler function for GET /api/v2/sbom/compare with query parameter extraction and validation
- `tests/api/sbom_compare.rs` -- integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the comparison route alongside existing SBOM routes
- `server/src/main.rs` -- ensure SBOM module routes (including comparison) are mounted (may already be handled by existing module mounting)
- `tests/Cargo.toml` -- add sbom_compare test module if needed

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- NEW: accepts two SBOM IDs as query parameters, returns `SbomComparisonResult` JSON

## Implementation Notes

The endpoint handler should:
1. Extract `left` and `right` query parameters (both required UUIDs or numeric IDs matching the existing SBOM ID format).
2. Validate that both parameters are present and are valid SBOM identifiers. Return `400 Bad Request` with a descriptive error if either is missing or invalid.
3. Validate that both SBOMs exist by fetching them via `SbomService`. Return `404 Not Found` if either SBOM does not exist.
4. Call the comparison service (from Task 2) with both SBOM IDs.
5. Return the `SbomComparisonResult` as JSON with `200 OK`.

Per CONVENTIONS.md §Endpoint Registration: register the comparison route in `endpoints/mod.rs` using the same pattern as existing routes (list.rs, get.rs). See `modules/fundamental/src/sbom/endpoints/mod.rs` for the route registration pattern.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

Per CONVENTIONS.md §Error Handling: return `Result<Json<SbomComparisonResult>, AppError>` from the handler, wrapping all errors with `.context()`. See `modules/fundamental/src/sbom/endpoints/get.rs` for the established handler pattern.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` endpoint scope.

Per CONVENTIONS.md §Testing: write integration tests in `tests/api/` that hit a real PostgreSQL test database, using the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern. See `tests/api/sbom.rs` for the established test structure.
Applies: task creates `tests/api/sbom_compare.rs` matching the convention's test file scope.

**Performance monitoring (NFR):** The comparison endpoint should respect the p95 < 1s target for SBOMs with up to 2000 packages each. Consider adding the endpoint to the API latency Grafana dashboard as noted in the feature's Customer Information section.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- existing SBOM GET endpoint handler; follow its pattern for query parameter extraction, error handling, and response format
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- existing route registration; add comparison route alongside existing routes
- `common/src/db/query.rs` -- shared query builder helpers if filtering or sorting is needed on comparison results
- `tests/api/sbom.rs` -- existing SBOM integration tests; follow test setup and assertion patterns

## Acceptance Criteria
- [ ] GET /api/v2/sbom/compare?left={id1}&right={id2} returns 200 with SbomComparisonResult JSON
- [ ] Returns 400 when left or right parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response shape matches the documented API contract (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] Route is registered and accessible via the API

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences, verify all diff categories are populated correctly
- [ ] Integration test: compare two identical SBOMs, verify all diff arrays are empty
- [ ] Integration test: compare with a non-existent SBOM ID, verify 404 response
- [ ] Integration test: missing query parameters, verify 400 response
- [ ] Integration test: compare SBOMs from different products/projects, verify the endpoint does not reject cross-product comparisons (business logic may filter, but the endpoint should not)

## Verification Commands
- `cargo test --test sbom_compare` -- run comparison endpoint integration tests
- `curl "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>"` -- verify endpoint returns valid JSON response

## Documentation Updates
- `tests/api/sbom_compare.rs` -- new test file documenting the comparison endpoint behavior through test cases

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 2 -- Add SBOM comparison model and diff service
