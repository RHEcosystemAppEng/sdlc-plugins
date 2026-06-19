## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Wire the SBOM comparison service into an Axum HTTP endpoint at `GET /api/v2/sbom/compare?left={id}&right={id}`. This endpoint extracts the two SBOM IDs from query parameters, calls the comparison service, and returns the structured diff as JSON.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Endpoint handler for GET /api/v2/sbom/compare

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the comparison route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/compare?left={id}&right={id}` — NEW: Returns JSON `SbomComparison` with added/removed packages, version changes, new/resolved vulnerabilities, and license changes

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`:
- Define an Axum handler function that extracts query parameters
- Use `axum::extract::Query` for the `left` and `right` query params
- Call `SbomService::compare()` from the service layer (task 3)
- Return `Result<Json<SbomComparison>, AppError>`

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for existing routes (`.route("/api/v2/sbom/compare", get(compare::handler))`).

Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` and modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint scope.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for handler function signature, query param extraction, and JSON response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `common/src/error.rs::AppError` — error type for handler return

## Dependencies
- Depends on: Task 3 — Backend comparison service (calls `SbomService::compare()`)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id}&right={id}` returns 200 with `SbomComparison` JSON
- [ ] Returns 400 when `left` or `right` query param is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Response Content-Type is `application/json`

## Test Requirements
- [ ] Handler unit test: valid left and right IDs return 200 with expected JSON structure
- [ ] Handler unit test: missing query parameter returns 400
- [ ] Handler unit test: non-existent SBOM ID returns 404
