## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs), calls the comparison service from Task 2, and returns the structured diff as JSON. Also add integration tests validating the endpoint behavior. The endpoint must meet the p95 < 1s performance requirement for SBOMs with up to 2000 packages each.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for GET /api/v2/sbom/compare

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the /compare route alongside existing /api/v2/sbom routes
- `tests/api/sbom.rs` — add integration tests for the comparison endpoint
- `server/src/main.rs` — ensure the sbom module routes include the new compare endpoint (if not auto-mounted via endpoints/mod.rs)

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns SbomComparisonResult JSON with six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
1. **Handler function**: create an async handler `compare` in `compare.rs` that:
   - Extracts `left` and `right` query parameters (both required UUIDs)
   - Validates both parameters are present; return 400 Bad Request if missing
   - Calls `SbomComparisonService::compare(left, right)` from Task 2
   - Returns the result as `Json<SbomComparisonResult>` with 200 OK
   - Returns 404 if either SBOM ID is not found
   - Returns 400 if both IDs are the same

   Follow the pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure and error mapping.

2. **Route registration**: in `modules/fundamental/src/sbom/endpoints/mod.rs`, add the compare route following the existing pattern used for `list.rs` and `get.rs`. Register it as `.route("/compare", get(compare::compare))` under the `/api/v2/sbom` scope.

3. **Integration tests**: follow the pattern in `tests/api/sbom.rs` which hits a real PostgreSQL test database and uses `assert_eq!(resp.status(), StatusCode::OK)`.

Per CONVENTIONS.md §Endpoint Registration: register the compare route in `endpoints/mod.rs` and ensure it is mounted via `server/main.rs`.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

Per CONVENTIONS.md §Error Handling: the handler must return `Result<Json<SbomComparisonResult>, AppError>` with `.context()` wrapping on service calls.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Testing: add integration tests in `tests/api/` following the existing test patterns with real database.
Applies: task modifies `tests/api/sbom.rs` matching the convention's integration test scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference handler for single-SBOM endpoint; follow its pattern for error mapping and response types
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference handler for list endpoint; follow its query parameter extraction pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — shared error type for endpoint responses
- `tests/api/sbom.rs` — existing SBOM integration tests; follow test setup and assertion patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with SbomComparisonResult JSON
- [ ] Missing `left` or `right` query parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Same SBOM ID for both left and right returns 400 Bad Request
- [ ] Response JSON matches the expected shape from the Feature description (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] Endpoint is registered under /api/v2/sbom/compare and accessible

## Test Requirements
- [ ] Integration test: compare two valid SBOMs returns 200 with correct diff structure
- [ ] Integration test: missing left parameter returns 400
- [ ] Integration test: missing right parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: same ID for both parameters returns 400
- [ ] Integration test: compare SBOMs with known package differences returns correct added/removed/changed counts

## Verification Commands
- `cargo test --test api -- sbom::compare` — runs comparison endpoint integration tests
- `curl "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>"` — verify endpoint returns JSON diff

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model and diff service
