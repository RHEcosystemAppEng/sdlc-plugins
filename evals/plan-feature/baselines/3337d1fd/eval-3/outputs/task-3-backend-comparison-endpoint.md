## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs) and returns the structured comparison result. This endpoint wires the comparison service to the HTTP layer and includes integration tests against a real PostgreSQL test database.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler for `GET /api/v2/sbom/compare` with query parameter extraction
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route in the SBOM endpoint router
- `tests/api/mod.rs` — Add `mod sbom_compare;` if a test module index exists (otherwise the test file is auto-discovered)

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns a structured diff between two SBOMs as `SbomComparisonResult` JSON. Returns 400 if either query parameter is missing, 404 if either SBOM ID does not exist.

## Implementation Notes
Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`. The handler should:

1. Extract `left` and `right` from query parameters using Axum's `Query` extractor. Return 400 Bad Request if either is missing.
2. Call `SbomComparisonService::compare(db, left, right)` from `modules/fundamental/src/sbom/service/compare.rs`.
3. Return `Json(result)` on success, or propagate the `AppError` (which implements `IntoResponse` per `common/src/error.rs`).

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing `/api/v2/sbom` routes, using `.route("/compare", get(compare_handler))`.

For integration tests in `tests/api/sbom_compare.rs`, follow the pattern in `tests/api/sbom.rs`: use `assert_eq!(resp.status(), StatusCode::OK)` for success cases and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for missing SBOMs.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Reference for handler pattern and query extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern
- `common/src/error.rs::AppError` — Error handling with IntoResponse
- `tests/api/sbom.rs` — Integration test patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response JSON shape matches the contract defined in the Figma design context
- [ ] Route is registered in the SBOM endpoint module

## Test Requirements
- [ ] Integration test: successful comparison returns 200 with correct JSON structure
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: comparison of two SBOMs with known differences returns expected diff categories

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test --test api -- sbom_compare` — integration tests pass
- `curl "http://localhost:8080/api/v2/sbom/compare?left=1&right=2"` — returns JSON response

## Dependencies
- Depends on: Task 2 — Backend SBOM comparison service logic
