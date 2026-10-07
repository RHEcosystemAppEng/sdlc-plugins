## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the REST endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that accepts two SBOM IDs as query parameters and returns the structured comparison diff computed by the comparison service (Task 2). The endpoint follows the existing Axum handler pattern and integrates with the SBOM module's route registration.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler for `GET /api/v2/sbom/compare` with query parameter extraction and JSON response
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route in the SBOM router

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` JSON with added/removed packages, version changes, new/resolved vulnerabilities, and license changes

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/`. The `list.rs` and `get.rs` files demonstrate the Axum handler conventions: extract query/path parameters, call the service, return JSON.

Per the repo's endpoint registration convention: each module's `endpoints/mod.rs` registers routes; the handler goes in a separate file.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust endpoint file scope.

Per the repo's error handling convention: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust handler file scope.

Per the repo's testing convention: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/sbom_compare.rs` matching the convention's Rust test file scope.

**Handler implementation pattern** (following `get.rs`):
```rust
pub async fn compare(
    Query(params): Query<CompareParams>,
    service: Extension<SbomService>,
) -> Result<Json<SbomComparisonResult>, AppError> {
    let result = service.compare(params.left, params.right).await
        .context("comparing SBOMs")?;
    Ok(Json(result))
}
```

**Query parameters:**
- `left` — UUID of the left (baseline) SBOM
- `right` — UUID of the right (comparison target) SBOM
- Both are required; return 400 if either is missing

**Route registration** (in `endpoints/mod.rs`):
Add `.route("/compare", get(compare::compare))` to the existing SBOM router alongside the list and get routes.

**Error responses:**
- 400 Bad Request if either `left` or `right` parameter is missing
- 404 Not Found if either SBOM ID does not exist
- 500 Internal Server Error for unexpected failures

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler pattern for SBOM detail; demonstrates query parameter extraction and service call
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing GET handler for SBOM list; demonstrates JSON response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `tests/api/sbom.rs` — existing SBOM integration tests to follow as test structure template
- `common/src/error.rs::AppError` — shared error type used in all handlers

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response JSON matches the expected shape defined in the Figma backend interactions
- [ ] Route is registered in the SBOM module's route configuration
- [ ] Integration tests pass against the test database

## Test Requirements
- [ ] Integration test: successful comparison of two valid SBOMs returns 200 with correct diff structure
- [ ] Integration test: missing `left` parameter returns 400
- [ ] Integration test: missing `right` parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: verify response JSON contains all six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Verification Commands
- `cargo test --test sbom_compare` — all integration tests pass
- `curl 'http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>'` — returns valid JSON comparison result

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model and diff service
