## Repository
trustify-backend

## Target Branch
main

## Description
Create the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler and register it in the SBOM module's route configuration. The handler extracts the SBOM ID path parameter and optional `threshold` query parameter, calls `SbomService::advisory_severity_summary`, and returns the `AdvisorySeveritySummary` as JSON. The response is cached for 5 minutes using the existing tower-http caching middleware.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Handler function `advisory_summary` that accepts path param `id` (Uuid) and optional query param `threshold` (String), calls `SbomService::advisory_severity_summary`, and returns `Json<AdvisorySeveritySummary>`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `mod advisory_summary;` declaration and register the `GET /api/v2/sbom/{id}/advisory-summary` route with 5-minute cache configuration

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with optional `?threshold=critical|high|medium|low` query parameter

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` which implements `GET /api/v2/sbom/{id}`. Mirror its handler signature (Axum extractors for path params, state, etc.), error handling (`Result<Json<T>, AppError>`), and OpenAPI documentation attributes.

For route registration, follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` which registers routes for list and get operations. Add the new advisory-summary route as a nested route under `/api/v2/sbom/{id}/`.

For the 5-minute cache, follow the caching pattern described in the conventions: use `tower-http` caching middleware configured in the endpoint route builder, similar to how existing endpoints configure caching.

Per CONVENTIONS.md §Endpoint registration: register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` Rust scope.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` from the handler.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` Rust scope.

Per CONVENTIONS.md §Caching: use `tower-http` caching middleware with cache configuration in the endpoint route builder for the 5-minute cache requirement.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` Rust scope.

Per CONVENTIONS.md §Framework: use Axum extractors and handler patterns.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` Rust scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing SBOM GET handler; follow its extractor pattern, error handling, and OpenAPI attributes
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern for SBOM sub-routes
- `common/src/error.rs::AppError` — Error type implementing `IntoResponse` for Axum compatibility

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns `200 OK` with correct JSON shape
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical counts
- [ ] Returns `404 Not Found` when SBOM ID does not exist
- [ ] Response includes cache headers indicating 5-minute cache duration
- [ ] Handler follows the same extractor and error handling patterns as existing SBOM endpoints

## Test Requirements
- [ ] Verify the route is reachable and returns the expected JSON structure
- [ ] Verify 404 response for non-existent SBOM ID

## Dependencies
- Depends on: Task 2 — Advisory summary service (requires `SbomService::advisory_severity_summary` method)
