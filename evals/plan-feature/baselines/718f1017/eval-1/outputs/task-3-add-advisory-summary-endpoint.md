# Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching

## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the `SbomService::get_advisory_summary` method, applies a 5-minute cache using the existing tower-http caching middleware, and supports an optional `?threshold` query parameter to filter counts by minimum severity level.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route in the existing SBOM route tree with 5-minute cache configuration

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — implement the `get_advisory_summary` handler function that extracts the SBOM ID from the path, optional `threshold` from query parameters, calls `SbomService::get_advisory_summary`, and returns the `AdvisorySeveritySummary` as JSON

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 status; returns 404 if SBOM ID does not exist; supports optional `?threshold=critical|high|medium|low` query parameter to filter counts to only severity levels at or above the threshold

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`) — it extracts the SBOM ID from the Axum path parameter and calls the corresponding service method
- Follow the route registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — existing routes are registered here and mounted by `server/src/main.rs`
- For caching: use the existing tower-http caching middleware as described in the repository's Key Conventions. Configure a 5-minute `Cache-Control: max-age=300` header on the route builder
- Define a query parameter struct (e.g., `AdvisorySummaryQuery`) with an `Option<SeverityThreshold>` field for the `threshold` parameter, using Axum's `Query` extractor
- The handler should return `Result<Json<AdvisorySeveritySummary>, AppError>` consistent with the error handling convention
- Per the repository's Key Conventions (Endpoint registration): register the route in the SBOM module's `endpoints/mod.rs` so it is automatically mounted by `server/src/main.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.
- Per the repository's Key Conventions (Error handling): handler returns `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` endpoint file scope.
- Per the repository's Key Conventions (Caching): uses tower-http caching middleware with cache configuration in endpoint route builders.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler for SBOM details; demonstrates path parameter extraction and service method invocation pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing list handler; demonstrates query parameter extraction pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern and cache middleware application
- `common/src/error.rs::AppError` — error type that implements `IntoResponse` for Axum

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response includes `Cache-Control: max-age=300` header (5-minute cache)
- [ ] Optional `?threshold=critical` query parameter filters counts to only critical severity (other levels are zero)
- [ ] Endpoint is registered in the SBOM route tree and accessible via the Axum server

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct severity counts for a known SBOM
- [ ] Integration test: returns 404 for non-existent SBOM ID with consistent error response format
- [ ] Integration test: `?threshold=high` returns counts only for critical and high severities
- [ ] Integration test: response includes cache control header

## Verification Commands
- `cargo test --test api -- advisory_summary` — expected: all advisory summary integration tests pass
- `cargo build` — expected: project compiles without errors

## Documentation Updates
- `README.md` — add the new endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 2 — Add advisory severity aggregation service method

<!-- [sdlc-workflow] Description digest: sha256-md:9bf49dc6781e8ead6114c1f7d768b4503e0c36173088a1d772a458b065157ae2 -->
