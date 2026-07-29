## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint that exposes the SBOM comparison functionality via the REST API. The endpoint accepts two SBOM IDs as query parameters, delegates to the SbomService comparison method, and returns the structured diff result as JSON.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route alongside existing `/api/v2/sbom` routes

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns SbomComparisonResult JSON with six diff sections (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/get.rs` for handler function structure.
- The handler should:
  1. Extract `left` and `right` query parameters (both required, return 400 if missing)
  2. Call `SbomService::compare(left, right)` 
  3. Return the `SbomComparisonResult` as JSON with status 200
  4. Return 404 if either SBOM ID is not found
  5. Return 400 if both parameters point to the same SBOM
- Error handling: use `Result<Json<SbomComparisonResult>, AppError>` return type with `.context()` wrapping per the project convention.
- Route registration: add the compare route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing list and get routes. The route should be registered before the `/{id}` route to avoid path conflicts.
- The endpoint does NOT return `PaginatedResults<T>` — it returns the full comparison result. This is intentional since the comparison is a single computed result, not a list. For large diffs (>100 package changes per section), the frontend handles virtualization.
- Per the NFR: p95 response time < 1s for SBOMs with up to 2000 packages each.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the endpoint handler pattern with Axum extractors and AppError return type
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates the list endpoint pattern with query parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — shows route registration pattern for adding new routes
- `common/src/error.rs::AppError` — error enum implementing IntoResponse for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with SbomComparisonResult JSON
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 400 when `left` and `right` are the same SBOM ID
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Route is registered in the SBOM endpoints module
- [ ] Response Content-Type is application/json

## Test Requirements
- [ ] Integration test: valid comparison returns 200 with expected JSON shape
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: same SBOM ID for both parameters returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: verify response matches the SbomComparisonResult schema

## Verification Commands
- `cargo build -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental` — all tests pass
- `cargo test --test api sbom` — integration tests for SBOM endpoints pass

## Documentation Updates
- `tests/api/sbom.rs` — add integration tests for the comparison endpoint

## Dependencies
- Depends on: Task 2 — Backend comparison service (SbomService::compare method must exist)
