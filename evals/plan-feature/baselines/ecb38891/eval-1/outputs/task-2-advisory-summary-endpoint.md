## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` that calls the `SbomService::get_advisory_summary` method created in Task 1 and returns the `AdvisorySeveritySummary` response. Configure 5-minute cache middleware using tower-http on the endpoint route. Register the route in the SBOM module's endpoint registration.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `advisory-summary` route under `/api/v2/sbom/{id}/advisory-summary` with 5-minute cache configuration

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `AdvisorySeveritySummary` JSON response with 5-minute cache header

## Implementation Notes
- The endpoint handler should extract the SBOM ID from the URL path, call `SbomService::get_advisory_summary`, and return the result as JSON.
- Apply 5-minute (300-second) cache middleware using tower-http's caching layer, configured in the route builder. Follow the caching pattern used by existing endpoints in `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Return appropriate HTTP status codes: 200 for success, 404 when SBOM not found (propagated from the service method's `AppError::NotFound`).
- Per repo Key Conventions §Endpoint registration: each module's `endpoints/mod.rs` registers routes. Register the new route alongside existing SBOM routes in `modules/fundamental/src/sbom/endpoints/mod.rs`. See the existing `get.rs` endpoint registration for the pattern.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.
- Per repo Key Conventions §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. The handler should follow the same pattern as `modules/fundamental/src/sbom/endpoints/get.rs`.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` file scope.
- Per repo Key Conventions §Caching: uses tower-http caching middleware with cache configuration in endpoint route builders. Apply a 5-minute max-age cache directive.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for endpoint handler pattern (path extraction, service call, JSON response)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration and cache configuration

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `AdvisorySeveritySummary` JSON for a valid SBOM ID
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Response includes cache headers with a 5-minute (300-second) max-age
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`

## Test Requirements
- [ ] Integration test verifying 200 response with correct JSON shape for a valid SBOM
- [ ] Integration test verifying 404 response for a non-existent SBOM ID
- [ ] Integration test verifying cache headers are present in the response

## Verification Commands
- `cargo build --workspace` — project compiles without errors
- `cargo test -p fundamental` — fundamental module tests pass

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service
