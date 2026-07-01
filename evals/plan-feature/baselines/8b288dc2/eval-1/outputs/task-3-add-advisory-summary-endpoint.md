## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the service method from Task 2, applies 5-minute cache headers via tower-http caching middleware, and supports an optional `?threshold` query parameter to filter counts above a given severity level. Returns 404 for non-existent SBOM IDs.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route in the existing sbom route group

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for the advisory-summary endpoint

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with 200 OK
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: returns filtered counts including only severities at or above the specified threshold

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` (for single-resource GET) and `modules/fundamental/src/sbom/endpoints/list.rs` (for route registration in `mod.rs`).
- The handler should accept the SBOM ID as a path parameter and an optional `threshold` query parameter.
- Call `SbomService::get_advisory_summary()` from the handler and return the `AdvisorySeveritySummary` as JSON.
- For the `?threshold` parameter: when present, zero out counts for severities below the threshold. Severity ordering: critical > high > medium > low. For example, `?threshold=high` returns critical and high counts, with medium and low zeroed out. Recalculate `total` to reflect only the included severities.
- Apply 5-minute cache using tower-http caching middleware, following the existing cache configuration pattern in the endpoint route builders.
- Return 404 (propagated from the service layer error) when the SBOM ID does not exist.
- Per CONVENTIONS.md §Endpoint registration: register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing pattern. `server/main.rs` mounts all modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration file scope.
- Per CONVENTIONS.md §Error handling: handler returns `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for single-resource GET handler pattern, path parameter extraction, and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `common/src/error.rs::AppError` — error type for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body containing `critical`, `high`, `medium`, `low`, `total` fields
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response includes cache headers indicating 5-minute TTL
- [ ] Optional `?threshold` parameter filters severity counts correctly
- [ ] Route is registered in the sbom endpoints module

## Test Requirements
- [ ] Integration test: valid SBOM returns 200 with correct severity counts
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: threshold parameter filters counts correctly (e.g., `?threshold=high` returns only critical and high)
- [ ] Integration test: response includes appropriate cache headers

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental` — endpoint tests pass

## Documentation Updates
- `README.md` — add the new endpoint to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 2 — Add severity aggregation service method

[sdlc-workflow] Description digest: sha256-md:bf909f21b7d1107cdd197cd60dd9d0040e0cb33be1ded0c5c305615b89ffa582
