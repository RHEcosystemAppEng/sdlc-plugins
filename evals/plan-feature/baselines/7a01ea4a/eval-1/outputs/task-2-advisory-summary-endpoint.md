## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns aggregated severity counts for a given SBOM. The endpoint calls the `SbomService::get_advisory_summary` method (created in Task 1), applies a 5-minute cache using `tower-http` caching middleware, and returns a 404 if the SBOM ID does not exist. This is the primary MVP endpoint enabling dashboard widgets to render severity breakdowns without client-side counting.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function for `GET /api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the service method, and returns `Json<AdvisorySeveritySummary>` with a 5-minute cache header

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `advisory-summary` route under the existing `/api/v2/sbom` router with `tower-http` caching middleware configured for 5-minute TTL

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with `Content-Type: application/json`. Returns 404 if SBOM ID does not exist. Response is cached for 5 minutes via `Cache-Control` headers.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for the handler structure: extract path parameters, call the service, return JSON response with error handling.
- Use the existing route registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` where routes are registered for `/api/v2/sbom`. Add the new route alongside `list.rs` and `get.rs`.
- Apply `tower-http` caching middleware to the route with a 5-minute TTL, following the caching configuration pattern used by existing endpoint route builders.
- The handler should return `Result<Json<AdvisorySeveritySummary>, AppError>` — the `AppError` enum in `common/src/error.rs` already implements `IntoResponse` and handles 404 mapping.
- Per Key Conventions (Endpoint registration): each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per Key Conventions (Error handling): all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint file scope.
- Per Key Conventions (Caching): uses `tower-http` caching middleware; cache configuration in endpoint route builders.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler pattern for single-SBOM endpoints (path extraction, service call, JSON response)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern showing how to add new routes to the SBOM router
- `common/src/error.rs::AppError` — error type that maps to HTTP status codes including 404

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` for a valid SBOM
- [ ] Endpoint returns 404 with appropriate error body when SBOM ID does not exist
- [ ] Response includes cache headers indicating a 5-minute TTL
- [ ] Endpoint is registered and accessible via the existing route structure

## Test Requirements
- [ ] Integration test: valid SBOM returns 200 with correct severity counts
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: response contains proper cache control headers
- [ ] Integration test: response shape matches `{ critical: N, high: N, medium: N, low: N, total: N }`

## Verification Commands
- `cargo test --test api sbom_advisory_summary` — all integration tests pass
- `curl -v http://localhost:8080/api/v2/sbom/{id}/advisory-summary` — returns 200 with JSON body and cache headers

## Documentation Updates
- `docs/api/` — add the new endpoint to the REST API reference documenting path, parameters, response shape, and caching behavior

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
