## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the `SbomService::get_advisory_summary` method (from Task 1), applies a 5-minute cache, and supports an optional `?threshold=<severity>` query parameter for filtering counts above a severity level. This implements the primary deliverable of TC-9001.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler function for GET /api/v2/sbom/{id}/advisory-summary with query parameter extraction and 5-minute cache configuration

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route in the SBOM module's router

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with 5-minute cache; 404 if SBOM not found
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: filters counts to include only severities at or above the threshold

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler function signature, path parameter extraction, and error handling.
- Use Axum's `Query<>` extractor for the optional `threshold` query parameter. Define a query params struct (e.g., `AdvisorySummaryParams { threshold: Option<String> }`).
- Apply 5-minute cache using `tower-http` caching middleware, following the caching pattern used by other endpoints in the SBOM module. Configure cache control headers (max-age=300).
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes — follow the same pattern used for `list.rs` and `get.rs` route registration.
- The handler should call `SbomService::get_advisory_summary(id, threshold)` and return the `SeveritySummary` as JSON.
- Per CONVENTIONS.md §Error Handling: handler must return `Result<Json<SeveritySummary>, AppError>` with `.context()` wrapping on service calls. See `modules/fundamental/src/sbom/endpoints/get.rs` for the established pattern. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's .rs handler scope.
- Per CONVENTIONS.md §Endpoint Registration: register the route in `endpoints/mod.rs` and ensure `server/main.rs` mounts the SBOM module. See `modules/fundamental/src/sbom/endpoints/mod.rs` for the existing registration pattern. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Caching: use `tower-http` caching middleware for the 5-minute cache. Configure cache control in the endpoint route builder. See existing endpoint route builders in `modules/fundamental/src/sbom/endpoints/mod.rs` for the caching pattern. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's .rs endpoint scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler showing path parameter extraction, service call pattern, and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration showing how to add a new route to the SBOM router
- `common/src/error.rs::AppError` — shared error type with IntoResponse implementation

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ critical: N, high: N, medium: N, low: N, total: N }`
- [ ] Endpoint returns 404 when SBOM ID does not exist, consistent with existing SBOM endpoints
- [ ] Response includes cache control headers with max-age=300 (5 minutes)
- [ ] Optional `?threshold=critical` query parameter filters counts to include only critical-level advisories
- [ ] Response time p95 < 200ms for SBOMs with up to 500 advisories

## Test Requirements
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary returns 200 with correct severity counts
- [ ] Integration test: GET with non-existent SBOM ID returns 404
- [ ] Integration test: GET with ?threshold=critical returns only critical count
- [ ] Integration test: response includes appropriate cache headers

## Verification Commands
- `cargo test --test api advisory_summary` — all advisory-summary integration tests pass
- `curl -s http://localhost:8080/api/v2/sbom/{test-id}/advisory-summary | jq .` — verify response shape matches expected JSON structure

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
