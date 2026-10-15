## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that exposes the SBOM comparison service as a REST API. Register the route in the SBOM endpoint module and add integration tests verifying the endpoint returns correct comparison results, handles missing SBOMs, and meets the p95 < 1s performance requirement for SBOMs with up to 2000 packages.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for `GET /api/v2/sbom/compare` that extracts `left` and `right` query parameters, calls `SbomCompareService::compare`, and returns JSON response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route in the SBOM endpoint router
- `tests/api/sbom.rs` — Add integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Accepts two SBOM IDs as query parameters, returns `SbomComparisonResult` as JSON. Returns 404 if either SBOM ID does not exist. Returns 400 if either parameter is missing.

## Implementation Notes
- Per CONVENTIONS.md §Endpoint registration: register the compare route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing list and get routes. See the existing route registration pattern in that file.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.
- Per CONVENTIONS.md §Error handling: the handler must return `Result<Json<SbomComparisonResult>, AppError>` with `.context()` wrapping on service calls. See `modules/fundamental/src/sbom/endpoints/get.rs` for the pattern.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/sbom.rs` using the `assert_eq!(resp.status(), StatusCode::OK)` pattern against a real PostgreSQL test database. See existing tests in that file.
  Applies: task modifies `tests/api/sbom.rs` matching the convention's `.rs` test file scope.
- Use Axum `Query` extractor for the `left` and `right` parameters. Define a `CompareQuery` struct with `#[derive(Deserialize)]`:
  ```rust
  #[derive(Deserialize)]
  struct CompareQuery {
      left: Uuid,
      right: Uuid,
  }
  ```
- The endpoint does not use pagination (it returns the full diff), but the response structure follows the same JSON serialization conventions as other endpoints.
- No caching middleware for this endpoint — comparison results are dynamic and should not be cached.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Pattern for single-SBOM endpoint handler with error handling; adapt for dual-ID query parameters
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow when adding the compare route
- `common/src/error.rs::AppError` — Standard error type for endpoint handlers

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON when both SBOMs exist
- [ ] Returns 404 when the left SBOM ID does not exist
- [ ] Returns 404 when the right SBOM ID does not exist
- [ ] Returns 400 when the `left` query parameter is missing
- [ ] Returns 400 when the `right` query parameter is missing
- [ ] The compare route is registered in the SBOM endpoint router and accessible at the documented path
- [ ] Response JSON shape matches the contract defined in Task 1

## Test Requirements
- [ ] Integration test: compare two valid SBOMs — verify 200 response with correct diff structure
- [ ] Integration test: compare with non-existent left SBOM — verify 404 response
- [ ] Integration test: compare with non-existent right SBOM — verify 404 response
- [ ] Integration test: compare request missing query parameters — verify 400 response
- [ ] Integration test: compare two identical SBOMs — verify all diff arrays are empty

## Verification Commands
- `cargo test --test sbom` — Run SBOM integration tests including comparison endpoint tests

## Dependencies
- Depends on: Task 1 — Add SBOM comparison model and service
