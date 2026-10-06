## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` REST endpoint that accepts `left` and `right` query parameters (SBOM IDs), calls the comparison service from Task 2, and returns the structured diff as JSON. Also add integration tests that verify the endpoint against a real PostgreSQL test database.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — endpoint handler for `GET /api/v2/sbom/compare`
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the comparison route alongside existing SBOM routes
- `tests/api/mod.rs` or test entry point — add `mod sbom_compare;` to include the new test module (if applicable)

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` JSON with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## Implementation Notes
Per the backend endpoint registration convention: each module's `endpoints/mod.rs` registers routes, and `server/main.rs` mounts all modules. Add the comparison route in the SBOM endpoint module's route registration.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's endpoint file scope.

Per the backend error handling convention: all handlers return `Result<T, AppError>` with `.context()` wrapping. Return 400 Bad Request when query params are missing or invalid; return 404 when an SBOM ID is not found.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust handler scope.

Per the backend testing convention: integration tests in `tests/api/` hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/sbom_compare.rs` matching the convention's test file scope.

**Endpoint handler structure:**
1. Parse `left` and `right` from query parameters (use Axum's `Query` extractor)
2. Validate both parameters are present and non-empty
3. Call `SbomService::compare(left, right)`
4. Return the `SbomComparisonResult` as JSON with status 200

**Query parameter validation:**
- Missing `left` or `right`: return 400 with descriptive error message
- Same value for `left` and `right`: return 400 (comparing an SBOM to itself is not meaningful)

**Caching:** Per the backend caching convention, consider whether comparison results should be cached. Since diffs are computed on-the-fly and SBOM data may change (new advisories ingested), caching should be short-lived or absent. Start without caching.

See existing endpoint patterns in:
- `modules/fundamental/src/sbom/endpoints/get.rs` — example of a single-resource GET handler
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of query parameter extraction
- `tests/api/sbom.rs` — example of SBOM integration test patterns

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler pattern to follow for handler structure
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing query parameter extraction pattern
- `common/src/error.rs::AppError` — error enum with `IntoResponse` implementation for consistent error responses
- `tests/api/sbom.rs` — existing SBOM integration test patterns and test database setup

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Missing `left` or `right` query parameter returns 400
- [ ] Nonexistent SBOM ID returns 404
- [ ] Same value for `left` and `right` returns 400
- [ ] Response content type is `application/json`
- [ ] Response time is < 1s for SBOMs with up to 2000 packages each (p95 NFR)

## Test Requirements
- [ ] Integration test: successful comparison of two SBOMs with known diff returns correct response body
- [ ] Integration test: missing `left` param returns 400
- [ ] Integration test: missing `right` param returns 400
- [ ] Integration test: nonexistent left SBOM ID returns 404
- [ ] Integration test: nonexistent right SBOM ID returns 404
- [ ] Integration test: same SBOM ID for both params returns 400
- [ ] Integration test: comparison of two identical SBOMs returns empty diff categories

## Verification Commands
- `cargo test --test api sbom_compare` — run the comparison endpoint integration tests
- `cargo clippy -- -D warnings` — verify no lint warnings in new code

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model and diff service
