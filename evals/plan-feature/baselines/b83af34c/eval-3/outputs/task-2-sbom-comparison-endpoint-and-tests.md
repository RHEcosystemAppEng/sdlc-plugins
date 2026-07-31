## Repository
trustify-backend

## Target Branch
main

## Description
Create the `GET /api/v2/sbom/compare` REST endpoint for feature TC-9003 (SBOM comparison view) and write integration tests. The endpoint accepts `left` and `right` query parameters (SBOM IDs), calls the comparison service from Task 1, and returns the structured diff as JSON. This endpoint enables the frontend comparison UI and direct API consumption for compliance workflows.

**Priority**: Critical (inherited from TC-9003)
**Fix Version**: RHTPA 1.5.0 (inherited from TC-9003)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for `GET /api/v2/sbom/compare?left={id1}&right={id2}`, parses query params, calls `SbomCompareService::compare`, returns JSON response
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the comparison route alongside existing SBOM endpoints

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` JSON with added/removed packages, version changes, new/resolved vulnerabilities, and license changes

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/` where `list.rs` and `get.rs` demonstrate handler structure, query parameter parsing, and route registration.

The handler should:
1. Parse `left` and `right` from query parameters using Axum's `Query` extractor
2. Validate that both parameters are provided; return 400 if missing
3. Call `SbomCompareService::compare(left_id, right_id)` from Task 1
4. Return the `SbomComparisonResult` as JSON with status 200
5. Return 404 if either SBOM ID is not found (propagated from service error)

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following how `list.rs` and `get.rs` routes are registered — add `.route("/compare", get(compare::handler))` to the SBOM router.

Integration tests should follow the pattern in `tests/api/sbom.rs` — set up test database with known SBOM data, call the endpoint, assert on response status and body structure.

Per CONVENTIONS.md §Framework: use Axum extractors (Query, State) for the handler function signature. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust scope.

Per CONVENTIONS.md §Module pattern: follow the model/ + service/ + endpoints/ structure by placing the handler in endpoints/. Applies: convention has no file-type restriction (broadly applicable).

Per CONVENTIONS.md §Error handling: return `Result<Json<SbomComparisonResult>, AppError>` with `.context()` wrapping for fallible operations. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust syntax scope.

Per CONVENTIONS.md §Endpoint registration: register the comparison route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing pattern. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint file scope.

Per CONVENTIONS.md §Response types: follow the JSON serialization patterns from existing endpoints (e.g., `common/src/model/paginated.rs`) for the comparison response struct. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust scope.

Per CONVENTIONS.md §Query helpers: use query parameter parsing utilities from `common/src/db/query.rs` if applicable for input validation. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust scope.

Per CONVENTIONS.md §Testing: write integration tests in `tests/api/` that hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern. Applies: task creates `tests/api/sbom_compare.rs` matching the convention's test file scope.

Per CONVENTIONS.md §Caching: configure `tower-http` caching middleware for the comparison endpoint if appropriate (comparison results are deterministic for the same inputs). Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's endpoint route builder scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM endpoint handler; reuse as a structural template for the comparison handler
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration; follow the same pattern to add the comparison route
- `tests/api/sbom.rs` — existing SBOM integration tests; reuse test setup and assertion patterns
- `common/src/error.rs::AppError` — existing error type with IntoResponse implementation

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a valid `SbomComparisonResult` JSON response
- [ ] Missing `left` or `right` query parameter returns 400
- [ ] Non-existent SBOM ID returns 404
- [ ] Response JSON contains all six diff categories: added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes
- [ ] Endpoint is registered and accessible under the existing `/api/v2/sbom` route group
- [ ] p95 response time < 1s for SBOMs with up to 2000 packages each (performance acceptance)

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences — assert 200 and verify diff categories in response body
- [ ] Integration test: compare identical SBOMs — assert 200 and verify all diff arrays are empty
- [ ] Integration test: provide only `left` parameter — assert 400
- [ ] Integration test: provide non-existent SBOM ID — assert 404
- [ ] Integration test: verify response JSON structure matches expected schema (all six diff category keys present)

## Verification Commands
- `cargo test --test sbom_compare` — all integration tests pass
- `curl "http://localhost:8080/api/v2/sbom/compare?left=1&right=2"` — returns 200 with comparison JSON

## Dependencies
- Depends on: Task 1 — SBOM comparison model and diff service
