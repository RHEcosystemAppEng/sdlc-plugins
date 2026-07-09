## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler with 5-minute response caching. This endpoint calls `SbomService::advisory_severity_summary` (from Task 1) and returns the `AdvisorySeveritySummary` response. It returns 404 if the SBOM ID does not exist, consistent with existing SBOM endpoints. The response is cached for 5 minutes using the existing tower-http caching middleware.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler function that extracts the SBOM ID path parameter, calls the service method, and returns the response as JSON

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route with 5-minute cache configuration

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 OK, or 404 if SBOM not found

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction, error handling, and response serialization.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing SBOM routes. Follow the route registration pattern used for `GET /api/v2/sbom/{id}`.
- For the 404 case, check if the SBOM exists before querying advisory counts, or handle the "not found" case in the service method. Use the same error pattern as the existing `get` handler.
- Configure 5-minute cache using tower-http caching middleware in the route builder, following the pattern described in the codebase's caching setup.
- The handler should return `Result<Json<AdvisorySeveritySummary>, AppError>` following the standard Axum handler signature.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` with `.context()` wrapping for all error paths.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md §Endpoint Registration: register the route in `endpoints/mod.rs` following the established pattern.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Caching: configure cache using tower-http middleware in the endpoint route builder.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint configuration scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET handler; follow its pattern for path parameter extraction and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for SBOM endpoints
- `common/src/error.rs::AppError` — error type with `IntoResponse` implementation

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` for a valid SBOM
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Response is cached for 5 minutes (cache headers set correctly)
- [ ] Response content type is `application/json`

## Test Requirements
- [ ] Integration test: endpoint returns 200 with correct severity counts for a known SBOM
- [ ] Integration test: endpoint returns 404 for a nonexistent SBOM ID
- [ ] Integration test: repeated requests within 5 minutes return cached response

## Documentation Updates
- `README.md` — add the new endpoint to the API endpoint list if one exists

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and service method
