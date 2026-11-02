## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint handler for the SBOM comparison feature (TC-9003). This endpoint accepts two SBOM IDs as query parameters, invokes the `SbomService::compare` method, and returns the `SbomComparisonResult` as JSON.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — endpoint handler function for `GET /api/v2/sbom/compare`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the comparison route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: accepts two SBOM UUIDs as query parameters, returns `SbomComparisonResult` JSON

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/`:
- `get.rs` defines the `GET /api/v2/sbom/{id}` handler — use the same Axum extractor pattern for the handler function signature
- `list.rs` defines the `GET /api/v2/sbom` list handler — reference for query parameter extraction
- `mod.rs` registers routes using Axum's `Router::new().route(...)` pattern — add the comparison route here
- Use `axum::extract::Query` to extract `left` and `right` query parameters as a typed struct (e.g., `CompareQuery { left: Uuid, right: Uuid }`)
- Call `SbomService::compare(query.left, query.right)` and return `Json(result)`
- Return 400 Bad Request if either query parameter is missing or not a valid UUID

Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's endpoint module scope.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust handler scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM endpoint handler, reference for Axum extractor pattern and error handling
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing list handler, reference for query parameter extraction
- `common/src/error.rs::AppError` — standard error type for all endpoint handlers

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns `SbomComparisonResult` JSON
- [ ] Returns 400 if `left` or `right` query parameter is missing
- [ ] Returns 400 if query parameter values are not valid UUIDs
- [ ] Returns 404 if either referenced SBOM does not exist (delegated to service layer)
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`

## Test Requirements
- [ ] Test successful comparison returns 200 with correct JSON shape
- [ ] Test missing query parameters return 400
- [ ] Test invalid UUID format returns 400
- [ ] Test non-existent SBOM ID returns 404

## Dependencies
- Depends on: Task 2 — Backend comparison service
