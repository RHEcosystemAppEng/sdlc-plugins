## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint that exposes the SBOM comparison service (Task 2) over HTTP. The endpoint accepts two SBOM IDs as query parameters and returns the structured diff as JSON. This endpoint is consumed by the frontend comparison UI.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new comparison route alongside existing SBOM routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler for `GET /api/v2/sbom/compare`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` JSON with added/removed packages, version changes, new/resolved vulnerabilities, and license changes

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/`. The `list.rs` and `get.rs` files demonstrate the handler structure:
1. Define a query parameter struct (e.g., `CompareQuery { left: String, right: String }`)
2. Implement the handler function that extracts query params, calls `SbomService::compare()`, and returns the result as JSON
3. Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes

The handler should validate that both `left` and `right` query parameters are provided and return a 400 Bad Request if either is missing. If either SBOM ID is not found, return 404.

Per CONVENTIONS.md (Key Conventions) -- Error handling: handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md (Key Conventions) -- Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint registration scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET handler; follow the same pattern for query parameter extraction and error handling
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing SBOM list handler; reference for route registration pattern
- `common/src/error.rs::AppError` — shared error type; use for 400/404 responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Missing `left` or `right` query parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Response Content-Type is `application/json`

## Test Requirements
- [ ] Request with valid left and right SBOM IDs returns 200 with structured diff
- [ ] Request missing `left` parameter returns 400
- [ ] Request missing `right` parameter returns 400
- [ ] Request with non-existent left SBOM ID returns 404
- [ ] Request with non-existent right SBOM ID returns 404

## Verification Commands
- `cargo check -p trustify-fundamental` — no compilation errors
- `cargo test -p trustify-fundamental -- sbom::endpoints::compare` — endpoint handler tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model and diff service
