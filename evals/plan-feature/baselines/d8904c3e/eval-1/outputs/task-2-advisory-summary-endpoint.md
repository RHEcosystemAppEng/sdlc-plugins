## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns advisory severity counts for a given SBOM. The endpoint calls `SbomService::advisory_severity_summary` (from Task 1) and returns the `AdvisorySeveritySummary` as JSON. A 5-minute cache is applied using tower-http caching middleware. The endpoint returns 404 when the SBOM ID does not exist, consistent with existing SBOM endpoints.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for `GET /api/v2/sbom/{id}/advisory-summary` with 5-minute cache configuration

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/advisory-summary` route under the existing `/api/v2/sbom/{id}` path prefix

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 5-minute cache; 404 if SBOM ID not found

## Implementation Notes
- Follow the endpoint handler pattern from `modules/fundamental/src/sbom/endpoints/get.rs` — the handler takes `Path<Uuid>` for the SBOM ID, calls the service method, and returns `Json<AdvisorySeveritySummary>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing pattern where `get.rs` and `list.rs` handlers are mounted. Add `.route("/{id}/advisory-summary", get(advisory_summary::handler))` alongside the existing `/{id}` route.
- Apply 5-minute cache using tower-http caching middleware. Follow the caching configuration pattern established in the existing endpoint route builders (referenced in the repo's Key Conventions).
- Per CONVENTIONS.md §Endpoint Registration: register the route in `endpoints/mod.rs` and mount it in the SBOM module router.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Error Handling: return `Result<Json<AdvisorySeveritySummary>, AppError>` from the handler.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Caching: use tower-http caching middleware for the 5-minute cache TTL.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint route builder scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference handler for single-SBOM endpoint pattern (Path extraction, service call, JSON response)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — implements `IntoResponse` for automatic error conversion

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with severity counts JSON for a valid SBOM ID
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response is cached for 5 minutes (subsequent requests within 5 minutes return cached data)
- [ ] Route is properly registered under the SBOM module router

## Test Requirements
- [ ] Integration test: GET request with valid SBOM ID returns 200 and correct JSON shape
- [ ] Integration test: GET request with non-existent SBOM ID returns 404
- [ ] Integration test: verify cache header indicates 5-minute max-age

## Verification Commands
- `cargo build -p fundamental` — compiles without errors
- `cargo test -p fundamental -- advisory_summary` — all tests pass

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and service method
