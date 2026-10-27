## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs) and returns a structured diff using `SbomComparisonService`. Register the route in the SBOM module's endpoint configuration.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler for GET /api/v2/sbom/compare

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the compare route alongside existing /api/v2/sbom routes

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns SbomComparison JSON with added/removed packages, version changes, new/resolved vulnerabilities, license changes

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` (list handler) and `modules/fundamental/src/sbom/endpoints/get.rs` (get handler) for Axum handler definition, query parameter extraction, and error response formatting.

The handler should:
1. Extract `left` and `right` query parameters as SBOM IDs
2. Validate both parameters are present; return 400 Bad Request if missing
3. Call `SbomComparisonService::compare(left, right)` 
4. Return the `SbomComparison` struct as JSON with 200 OK
5. Return 404 if either SBOM ID is not found

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing pattern where `list.rs` and `get.rs` routes are registered. The compare endpoint is a GET on a sub-path: `/api/v2/sbom/compare`.

Per CONVENTIONS.md §Endpoint Registration: register the route in the module's endpoints/mod.rs; server/main.rs mounts all modules.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint registration scope.

Per CONVENTIONS.md §Error Handling: handler returns `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing endpoint handler demonstrating query parameter extraction and response formatting
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing endpoint handler demonstrating path parameter extraction and 404 handling
- `common/src/error.rs::AppError` — error enum for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with SbomComparison JSON
- [ ] Returns 400 Bad Request when left or right parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Response JSON matches the expected shape defined in the SbomComparison model

## Test Requirements
- [ ] Integration test: valid comparison returns 200 with correct diff structure
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404

## Verification Commands
- `cargo test --test api` — run integration tests to verify endpoint behavior

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Backend comparison service
