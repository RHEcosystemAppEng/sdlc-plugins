## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare?left={id1}&right={id2}` REST endpoint that returns a structured SBOM comparison result. Register the endpoint in the SBOM module's route configuration and add integration tests covering success, validation, and error cases.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/compare` route alongside existing SBOM endpoints
- `tests/api/sbom.rs` — add integration tests for the comparison endpoint
- `server/src/main.rs` — verify SBOM module routes are mounted (no change expected if already mounting the module)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for `GET /api/v2/sbom/compare`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: accepts two SBOM IDs as query parameters, returns `SbomComparisonResult` JSON with six diff sections (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` for handler function structure.
  - Per CONVENTIONS.md §Endpoint Registration: register the compare route in `modules/fundamental/src/sbom/endpoints/mod.rs` using the same router builder pattern as list and get endpoints.
    Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` endpoint scope.
- The handler should:
  1. Parse `left` and `right` query parameters (both required; return 400 if missing)
  2. Call `SbomComparisonService::compare(left_id, right_id)` from Task 2
  3. Return the `SbomComparisonResult` as JSON with status 200
  4. Return 404 if either SBOM ID does not exist
  5. Return 400 if `left` and `right` are the same ID
- Per CONVENTIONS.md §Error Handling: return `Result<Json<SbomComparisonResult>, AppError>` with `.context()` wrapping on service calls.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` handler scope.
- Per CONVENTIONS.md §Testing: follow the integration test pattern in `tests/api/sbom.rs` using `assert_eq!(resp.status(), StatusCode::OK)` and real PostgreSQL test database.
  Applies: task modifies `tests/api/sbom.rs` matching the convention's `.rs` test file scope.
- Do NOT return `PaginatedResults<T>` — this endpoint returns a single comparison result, not a list.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler pattern for single-resource response; follow its Axum extractor and error handling structure
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing list handler for query parameter extraction pattern
- `common/src/error.rs::AppError` — error type for handler return values

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Missing `left` or `right` query parameter returns 400 with error message
- [ ] Nonexistent SBOM ID returns 404 with error message
- [ ] Same ID for `left` and `right` returns 400 with descriptive error
- [ ] Response body matches the expected JSON shape with all six diff sections
- [ ] Endpoint is registered and accessible through the SBOM module routes
- [ ] Response time p95 < 1s for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Integration test: compare two valid SBOMs returns 200 with correct diff structure
- [ ] Integration test: missing `left` parameter returns 400
- [ ] Integration test: missing `right` parameter returns 400
- [ ] Integration test: nonexistent SBOM ID returns 404
- [ ] Integration test: same ID for both parameters returns 400
- [ ] Integration test: large SBOM comparison (>100 packages) returns within acceptable time
- [ ] Integration test: comparison result contains correct added/removed packages counts

## Verification Commands
- `cargo test --test api sbom::compare` — run comparison endpoint integration tests
- `curl "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>"` — verify endpoint returns valid JSON response

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model types and diff service
