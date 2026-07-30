## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the REST endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that exposes the SBOM comparison service to API consumers. The endpoint accepts two SBOM IDs as query parameters, delegates to the `SbomService::compare()` method from Task 2, and returns the structured diff as JSON. This endpoint also serves as the backend contract for the frontend comparison page.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- handler function for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the comparison route alongside existing SBOM routes
- `tests/api/sbom.rs` -- add integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- NEW: returns `SbomComparisonResult` as JSON; 200 on success, 404 if either SBOM ID is not found, 400 if query parameters are missing

## Implementation Notes
Per CONVENTIONS.md Endpoint registration: register the comparison route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing pattern for `list.rs` and `get.rs`. The route is mounted under the `/api/v2/sbom` prefix.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` endpoint scope.

Per CONVENTIONS.md Error handling: the handler must return `Result<Json<SbomComparisonResult>, AppError>` and wrap errors with `.context()`.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md Testing pattern: add integration tests in `tests/api/sbom.rs` using the existing `assert_eq!(resp.status(), StatusCode::OK)` pattern, hitting a real PostgreSQL test database.
Applies: task modifies `tests/api/sbom.rs` matching the convention's `.rs` test file scope.

**Handler implementation:**
1. Extract `left` and `right` query parameters (return 400 if missing)
2. Call `SbomService::compare(left, right)` from the injected service
3. Return `Json(result)` on success
4. Map `AppError::NotFound` to 404 response

**Route registration pattern** (reference `modules/fundamental/src/sbom/endpoints/mod.rs`):
```rust
.route("/compare", get(compare::handler))
```

**Note:** This endpoint does NOT return `PaginatedResults<T>` since it returns a single comparison result, not a list. The comparison result contains arrays internally but the top-level response is a single object.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- reference for handler function signature, query parameter extraction, and error response patterns
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference for route registration and handler wiring
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- existing route registration; add comparison route here
- `common/src/error.rs::AppError` -- existing error type for consistent error responses
- `tests/api/sbom.rs` -- existing SBOM integration tests; follow the same test setup and assertion patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response JSON matches the expected shape with all six diff categories
- [ ] Endpoint is registered and accessible under `/api/v2/sbom/compare`
- [ ] p95 response time < 1s for SBOMs with up to 2,000 packages (per non-functional requirements)

## Test Requirements
- [ ] Integration test: valid comparison request returns 200 with correct diff structure
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: comparison of two SBOMs with known differences returns expected diff counts
- [ ] Integration test: comparison of identical SBOMs returns empty diff sections

## Verification Commands
- `cargo test --test api sbom::compare` -- runs the comparison endpoint integration tests
- `curl "http://localhost:8080/api/v2/sbom/compare?left=1&right=2"` -- manual endpoint verification

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 2 -- Add SBOM comparison diff models and service
