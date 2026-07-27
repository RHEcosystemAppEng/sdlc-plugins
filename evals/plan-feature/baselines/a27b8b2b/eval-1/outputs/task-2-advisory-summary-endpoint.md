# Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching

## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns severity counts for a given SBOM. The endpoint delegates to the `SbomService::advisory_summary` method (created in Task 1), returns a JSON response matching the `AdvisorySeveritySummary` model, and is configured with a 5-minute `tower-http` cache. If the SBOM ID does not exist, the endpoint returns 404, consistent with existing SBOM endpoints.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function for `GET /api/v2/sbom/{id}/advisory-summary`; extracts SBOM ID from path, calls `SbomService::advisory_summary`, returns JSON response or 404

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `advisory_summary` route under `/api/v2/sbom/{id}/advisory-summary` with 5-minute `tower-http` cache middleware

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with `Content-Type: application/json`. Returns 404 if SBOM ID does not exist.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure: extract path parameters using Axum extractors, call the service method, return `Json<AdvisorySeveritySummary>` or `AppError`.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint scope.
- Route registration pattern: add the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern as the existing `GET /api/v2/sbom/{id}` route registration. See the `get.rs` route for the established pattern.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint registration scope.
- Caching: use `tower-http` caching middleware with a 5-minute TTL. The project uses `tower-http` for caching (see Key Conventions). Configure the cache layer on the route builder, similar to how other cached routes are configured.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's caching scope.
- Error handling: return `Result<Json<AdvisorySeveritySummary>, AppError>`. For 404, check if the SBOM exists first (or catch the not-found error from the service) and return an appropriate `AppError` variant. Follow the pattern in `get.rs`.
- The `server/src/main.rs` already mounts the sbom module's routes, so no changes are needed there — the new route will be picked up automatically from the sbom `endpoints/mod.rs` registration.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler for SBOM details; demonstrates the established pattern for path parameter extraction, service call, JSON response, and 404 handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration file; demonstrates how to add new routes with middleware

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct JSON shape for a valid SBOM
- [ ] Endpoint returns 404 when SBOM ID does not exist, consistent with existing SBOM endpoints
- [ ] Response is cached for 5 minutes using `tower-http` caching middleware
- [ ] Response Content-Type is `application/json`

## Test Requirements
- [ ] Integration test: valid SBOM returns 200 with correct severity counts
- [ ] Integration test: nonexistent SBOM ID returns 404
- [ ] Integration test: repeated requests within 5 minutes return cached response

## Verification Commands
- `cargo build -p fundamental` — compiles without errors
- `cargo test -p fundamental -- advisory_summary` — all tests pass

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and severity aggregation service method
