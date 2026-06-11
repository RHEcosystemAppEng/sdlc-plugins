# Task 4 — Add GET /api/v2/sbom/compare endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the REST endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that accepts two SBOM IDs as query parameters and returns the structured diff computed by the comparison service. Register the endpoint in the sbom module's route configuration.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for `GET /api/v2/sbom/compare` that parses query parameters, calls `SbomComparisonService::compare`, and returns the result as JSON

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the comparison route in the sbom endpoint router

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` as JSON. Query parameters `left` and `right` are required UUIDs. Returns 400 if either parameter is missing, 404 if either SBOM is not found.

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `list.rs` — use Axum extractors for query parameters, return `Result<Json<T>, AppError>`.
- Define a `CompareQuery` struct with `left: Uuid` and `right: Uuid` fields, using Axum's `Query` extractor to parse from URL query string.
- The handler should call `SbomComparisonService::compare(db, left, right)` and return the result wrapped in `Json`.
- Register the route as `.route("/api/v2/sbom/compare", get(compare))` in the sbom endpoint module's router. Ensure it is registered before the `/{id}` route to avoid path conflicts.
- Consider adding `tower-http` caching middleware for short-lived caching (e.g., 30 seconds) since comparison results are computed on-the-fly. Follow the caching pattern used by existing endpoint route builders.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for the handler pattern with Axum extractors and AppError return type
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for query parameter parsing and response serialization
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `common/src/error.rs::AppError` — error handling enum with IntoResponse implementation

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response body matches the expected JSON shape with all six diff categories
- [ ] Route is registered in the sbom endpoint module and does not conflict with existing routes

## Test Requirements
- [ ] Integration test: compare two valid SBOMs returns 200 with correct diff structure
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: verify response JSON shape matches `SbomComparisonResult` serialization

## Verification Commands
- `cargo test --test api sbom_compare` — expected: all comparison endpoint tests pass
- `cargo build` — expected: no compilation errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison service logic
