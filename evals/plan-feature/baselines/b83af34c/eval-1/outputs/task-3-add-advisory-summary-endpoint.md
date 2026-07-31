## Repository
trustify-backend

## Target Branch
main

## Priority
Major

## Fix Versions
RHTPA 1.5.0

## Description
Implement the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that calls the `SbomService::get_advisory_summary` method and returns the severity counts as JSON. Apply 5-minute cache-control headers using the existing `tower-http` caching middleware. Support an optional `?threshold` query parameter to filter severity counts at or above a given level.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `advisory_summary` route under the SBOM router

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`. Optional query parameter `?threshold=critical|high|medium|low` filters to counts at or above the specified severity.

## Implementation Notes
Create the handler function in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` following the pattern in `modules/fundamental/src/sbom/endpoints/get.rs`. The handler should:
1. Extract `{id}` path parameter using Axum's `Path` extractor
2. Optionally extract `threshold` from query parameters using Axum's `Query` extractor
3. Call `SbomService::get_advisory_summary(id)` to retrieve the aggregated counts
4. If a threshold is specified, zero out severity levels below the threshold and recompute the total
5. Return `Json(summary)` with appropriate status code

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` by adding `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::handler))` to the existing router, following the registration pattern used for `get.rs` and `list.rs` in the same module.

Apply `tower-http` cache-control with a 5-minute (`max-age=300`) TTL on the response, following the caching middleware pattern used in existing endpoint route builders.

Per CONVENTIONS.md §Framework: use Axum extractors (`Path`, `Query`) and `Json` response type. Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust syntax scope.

Per CONVENTIONS.md §Module pattern: place the endpoint handler in the `endpoints/` subdirectory of the `sbom` domain module. Applies: convention has no file-type restriction (broadly applicable).

Per CONVENTIONS.md §Error handling: handler returns `Result<Json<AdvisorySeveritySummary>, AppError>` with `.context()` wrapping on service errors. Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust syntax scope.

Per CONVENTIONS.md §Endpoint registration: register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Caching: apply `tower-http` caching middleware with 5-minute TTL in the endpoint route builder. Applies: convention has no file-type restriction (broadly applicable).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET handler to follow as a pattern for path extraction and response structure
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to replicate
- `common/src/error.rs::AppError` — error type implementing `IntoResponse` for 404 and other error cases

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{"critical": N, "high": N, "medium": N, "low": N, "total": N}`
- [ ] Returns 404 if SBOM ID does not exist
- [ ] Response includes `Cache-Control: max-age=300` header (5-minute TTL)
- [ ] Optional `?threshold=critical` query parameter returns only critical counts (other levels zeroed or filtered)
- [ ] Endpoint is registered and accessible in the SBOM router

## Test Requirements
- [ ] Verify 200 response with correct JSON shape for a valid SBOM ID
- [ ] Verify 404 response for nonexistent SBOM ID
- [ ] Verify cache-control header is present with correct max-age value
- [ ] Verify threshold query parameter filters severity counts correctly

## Dependencies
- Depends on: Task 2 — Implement advisory severity aggregation service method
