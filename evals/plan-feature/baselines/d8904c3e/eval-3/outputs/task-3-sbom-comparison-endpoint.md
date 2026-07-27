## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` REST endpoint that accepts `left` and `right` query parameters (SBOM IDs), calls the comparison service from Task 2, and returns the structured diff as JSON. Register the new route in the sbom module's endpoint configuration and add integration tests covering all diff categories.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- handler function for GET /api/v2/sbom/compare accepting Query<CompareParams> with left and right SBOM ID fields
- `tests/api/sbom_compare.rs` -- integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the /compare route in the sbom router, add `pub mod compare;`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- NEW: returns SbomComparisonResult JSON with six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
Per CONVENTIONS.md endpoint registration: register the compare route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern as the existing `list` and `get` routes. See the route registration pattern in that file.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md error handling: the handler must return `Result<Json<SbomComparisonResult>, AppError>` with `.context()` wrapping. See `modules/fundamental/src/sbom/endpoints/get.rs` for the established handler pattern.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md testing: integration tests go in `tests/api/` and use a real PostgreSQL test database. Follow the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in `tests/api/sbom.rs`.
Applies: task creates `tests/api/sbom_compare.rs` matching the convention's `.rs` test file scope.

**Handler implementation:**
- Define `CompareParams` struct with `left: String` and `right: String` fields, deriving `Deserialize`
- Extract query params via Axum's `Query<CompareParams>` extractor
- Call the comparison service's `compare()` method with both IDs
- Return 400 Bad Request if either query param is missing
- Return 404 Not Found if either SBOM ID does not exist (propagated from service's AppError)
- Return 200 OK with JSON body on success

**Performance:**
- No caching needed for comparison results since they are computed on-the-fly and inputs may change
- The service layer handles query batching for the p95 < 1s requirement

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- reference handler implementation for single-SBOM endpoint pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference for query parameter extraction pattern
- `common/src/db/query.rs` -- shared query builder helpers if needed for filtering
- `tests/api/sbom.rs` -- existing SBOM integration test patterns to follow

## Acceptance Criteria
- [ ] GET /api/v2/sbom/compare?left={id1}&right={id2} returns 200 with SbomComparisonResult JSON
- [ ] Endpoint returns 400 when left or right query parameter is missing
- [ ] Endpoint returns 404 when either SBOM ID does not exist
- [ ] Response JSON contains all six diff categories with correct data
- [ ] Route is registered under /api/v2/sbom/compare in the sbom module router

## Test Requirements
- [ ] Integration test: successful comparison of two SBOMs with known diff returns expected JSON structure
- [ ] Integration test: missing query parameter returns 400 status
- [ ] Integration test: non-existent SBOM ID returns 404 status
- [ ] Integration test: comparing an SBOM with itself returns empty diff arrays
- [ ] Integration test: response includes correct counts for each diff category

## Verification Commands
- `cargo test --test sbom_compare` -- runs the comparison endpoint integration tests, expects all tests to pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 2 -- Add SBOM comparison model and service
