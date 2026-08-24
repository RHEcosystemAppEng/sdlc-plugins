## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts two SBOM IDs as query parameters and returns a structured diff using the comparison service created in Task 2. Register the endpoint route and write integration tests.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — endpoint handler for `GET /api/v2/sbom/compare?left={id1}&right={id2}`
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/compare` route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` JSON with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## Implementation Notes
- Per CONVENTIONS.md §Endpoint Registration: register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Error Handling: the handler must return `Result<Json<SbomComparisonResult>, AppError>` and use `.context()` for error wrapping.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` must hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/sbom_compare.rs` matching the convention's test file scope.
- Extract `left` and `right` query parameters as UUID/string IDs. Validate both are present and return 400 Bad Request if either is missing.
- Return 404 if either SBOM ID does not exist.
- This endpoint does NOT return `PaginatedResults<T>` — it returns a single `SbomComparisonResult`. This is intentional since the comparison is not a list operation.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing endpoint handler pattern for single-SBOM retrieval, follow same structure
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration, add the compare route alongside
- `tests/api/sbom.rs` — existing SBOM integration tests, follow test setup and assertion patterns
- `common/src/error.rs::AppError` — error enum for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response JSON contains all six diff categories as defined in the model
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences, verify all diff categories
- [ ] Integration test: compare identical SBOMs, verify empty diff
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404

## Verification Commands
- `cargo test --test api sbom_compare` — run comparison endpoint integration tests

## Documentation Updates
- `README.md` — add the comparison endpoint to the API reference section (detailed documentation handled by Task 7)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison diff model and service
