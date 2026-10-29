## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the REST endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that exposes the SBOM comparison service as an HTTP API. The endpoint validates the query parameters, delegates to `SbomService::compare()`, and returns the structured diff as JSON. This endpoint enables the frontend comparison UI and direct API consumers to compare two SBOM versions.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for GET /api/v2/sbom/compare with query parameter extraction and validation
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the comparison route alongside existing SBOM routes
- `tests/api/mod.rs` — add `mod sbom_compare;` declaration (if module-based test organization is used)

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparison` JSON response with six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/`. The `get.rs` and `list.rs` handlers demonstrate the established patterns for parameter extraction, service calls, and response serialization.

The handler should:
1. Extract `left` and `right` query parameters (both required UUIDs)
2. Return 400 Bad Request if either parameter is missing or invalid
3. Call `SbomService::compare(left, right)` 
4. Return 404 Not Found if either SBOM does not exist (propagated from the service's AppError)
5. Return 200 OK with the `SbomComparison` JSON body

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing `/api/v2/sbom` routes. The route registration follows the pattern established by `list.rs` and `get.rs` in the same directory.

Integration tests follow the pattern in `tests/api/sbom.rs`: hit a real PostgreSQL test database and assert on response status and body structure using `assert_eq!(resp.status(), StatusCode::OK)`.

Per CONVENTIONS.md: register the new route in the module's `endpoints/mod.rs` and return `Result<T, AppError>` from the handler.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET handler; follow its pattern for parameter extraction and service delegation
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration; follow its pattern for adding the comparison route
- `common/src/error.rs::AppError` — existing error type implementing IntoResponse; reuse for 400/404 error responses
- `tests/api/sbom.rs` — existing SBOM integration tests; follow its test setup and assertion patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a valid SbomComparison JSON body
- [ ] Endpoint returns 400 Bad Request when `left` or `right` query parameter is missing
- [ ] Endpoint returns 400 Bad Request when `left` or `right` is not a valid SBOM identifier
- [ ] Endpoint returns 404 Not Found when either SBOM ID does not exist in the database
- [ ] Response JSON shape matches the contract: `{ added_packages: [...], removed_packages: [...], version_changes: [...], new_vulnerabilities: [...], resolved_vulnerabilities: [...], license_changes: [...] }`
- [ ] Endpoint responds within p95 < 1s for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Integration test: compare two existing SBOMs returns 200 with correct diff structure
- [ ] Integration test: compare with missing `left` parameter returns 400
- [ ] Integration test: compare with missing `right` parameter returns 400
- [ ] Integration test: compare with nonexistent SBOM ID returns 404
- [ ] Integration test: compare an SBOM with itself returns 200 with empty diff arrays
- [ ] Integration test: compare two SBOMs with known differences returns correct counts in each diff category

## Verification Commands
- `cargo test --test api sbom_compare` — all integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model and diff service
