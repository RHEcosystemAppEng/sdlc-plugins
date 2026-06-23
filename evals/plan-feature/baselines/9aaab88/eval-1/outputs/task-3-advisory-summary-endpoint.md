## Repository
trustify-backend

## Target Branch
main

## Description
Create the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint delegates to the service method from Task 2, applies 5-minute cache headers, supports an optional `?threshold` query parameter, and returns 404 for non-existent SBOMs.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function `get_advisory_summary` that extracts the SBOM ID from the path, optional `threshold` query param, calls `SbomService::get_advisory_summary`, and returns `Json<AdvisorySeveritySummary>` with cache-control headers

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new route `GET /api/v2/sbom/{id}/advisory-summary` by adding the handler to the SBOM router, with 5-minute `tower-http` cache layer

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`. Supports optional `?threshold=critical|high|medium|low` query parameter to filter counts to severities at or above the threshold. Returns 404 if SBOM ID does not exist. Response cached for 5 minutes via Cache-Control headers.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — it shows how to extract a path parameter (`sbom_id`), call a service method, and return a JSON response with proper error handling.
- Route registration follows the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — existing routes like `list.rs` and `get.rs` are mounted here; add the new advisory-summary route in the same manner.
- For caching, follow the pattern described in Key Conventions (Caching): use `tower-http` caching middleware. Apply a 5-minute `Cache-Control: max-age=300` directive at the route level, consistent with how other cached endpoints are configured in route builders.
- For the `threshold` query parameter, define a query struct (e.g., `AdvisorySummaryQuery`) with an `Option<String>` field, following the pattern used for query parameters in other endpoint handlers.
- The endpoint must be registered in `modules/fundamental/src/sbom/endpoints/mod.rs` so that `server/src/main.rs` (which mounts all module routers) picks it up automatically.
- Per Key Conventions (Endpoint registration): each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` file scope.
- Per Key Conventions (Error handling): all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` file scope.
- Per Key Conventions (Caching): uses `tower-http` caching middleware; cache configuration in endpoint route builders. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Pattern for path parameter extraction, service call, and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern for the SBOM module
- `common/src/error.rs::AppError` — Standard error handling with `IntoResponse`

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` endpoint exists and returns JSON with severity counts
- [ ] Response shape is `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Endpoint returns HTTP 404 when SBOM ID does not exist
- [ ] Response includes `Cache-Control: max-age=300` header for 5-minute caching
- [ ] Optional `?threshold` query parameter filters severity counts to those at or above the specified level
- [ ] Endpoint is registered in SBOM module routes and accessible through the server

## Test Requirements
- [ ] Integration test verifying successful response with correct severity counts for an SBOM with known advisories
- [ ] Integration test verifying 404 response for a non-existent SBOM ID
- [ ] Integration test verifying `Cache-Control` header is present with `max-age=300`
- [ ] Integration test verifying `?threshold=critical` returns only critical count (others zero or omitted)

## Verification Commands
- `cargo test -p trustify-fundamental -- advisory_summary` — runs unit tests for the new endpoint
- `curl -s http://localhost:8080/api/v2/sbom/{id}/advisory-summary | jq .` — returns severity breakdown JSON

## Dependencies
- Depends on: Task 1 — Advisory severity model (requires `AdvisorySeveritySummary` struct)
- Depends on: Task 2 — Advisory severity service (requires `SbomService::get_advisory_summary` method)


[sdlc-workflow] Description digest: sha256-md:8f872cd867e33c7db517f1a35e795d00d70f32695457ddd5f4a717a2d587ddae
