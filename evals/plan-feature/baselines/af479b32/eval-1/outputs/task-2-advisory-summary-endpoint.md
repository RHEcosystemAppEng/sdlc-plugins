## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint calls `SbomService::advisory_severity_summary()` (from Task 1), returns the `AdvisorySeveritySummary` as JSON, configures a 5-minute `tower-http` cache, and returns 404 when the SBOM ID does not exist. This is the core MVP deliverable for TC-9001.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function `get_advisory_summary` that extracts the SBOM ID from the path, calls the service method, and returns the response with 5-minute cache headers

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `GET /api/v2/sbom/{id}/advisory-summary` route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with `Content-Type: application/json`. Returns 404 if SBOM ID does not exist. Response is cached for 5 minutes via `tower-http` cache-control headers.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for the handler structure: extract path parameter, call service, return `Result<Json<T>, AppError>`.
- Per Key Conventions §Endpoint registration: register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs`. The route path should be `.route("/api/v2/sbom/{id}/advisory-summary", get(get_advisory_summary))`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint registration scope.
- Per Key Conventions §Caching: use `tower-http` caching middleware to set `Cache-Control: max-age=300` on the response. Reference the existing cache configuration pattern in endpoint route builders.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint file scope.
- Per Key Conventions §Error handling: the handler returns `Result<Json<AdvisorySeveritySummary>, AppError>`. The `AppError::NotFound` from the service layer automatically maps to HTTP 404 via the `IntoResponse` implementation in `common/src/error.rs`.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint file scope.
- The endpoint does not use pagination (single summary object), so do not import or use `PaginatedResults<T>`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing `GET /api/v2/sbom/{id}` handler; direct pattern reference for path extraction, service invocation, and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for SBOM endpoints
- `common/src/error.rs::AppError` — error type with `IntoResponse` implementation for automatic HTTP status code mapping

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns `200 OK` with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` for a valid SBOM
- [ ] Endpoint returns `404 Not Found` when the SBOM ID does not exist
- [ ] Response includes `Cache-Control: max-age=300` header (5-minute cache)
- [ ] Response `Content-Type` is `application/json`
- [ ] Endpoint is registered and reachable in the Axum router

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct severity counts for an SBOM with known advisories
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for a nonexistent SBOM ID
- [ ] Integration test: response includes `Cache-Control` header with `max-age=300`

## Verification Commands
- `cargo test --test api advisory_summary` — verify integration tests pass
- `curl -v http://localhost:8080/api/v2/sbom/{id}/advisory-summary` — verify endpoint returns expected JSON shape and cache headers

## Documentation Updates
- `docs/api/` or OpenAPI spec — add `GET /api/v2/sbom/{id}/advisory-summary` endpoint documentation with request/response schema

## Dependencies
- Depends on: Task 1 — Add severity aggregation model and service method
