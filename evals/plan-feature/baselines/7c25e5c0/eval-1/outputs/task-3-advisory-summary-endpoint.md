## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint calls `SbomService::advisory_summary` and returns the `AdvisorySeveritySummary` response. Configure 5-minute `tower-http` caching on the route.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — new endpoint handler for the advisory summary route

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route and add `pub mod advisory_summary;`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `AdvisorySeveritySummary { critical, high, medium, low, total }` with 5-minute cache

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`) for handler function signature, path extraction, service injection, and error response
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern alongside the `list.rs` and `get.rs` routes
- Apply 5-minute `tower-http` cache configuration on the route — reference existing cache configuration patterns in the endpoint route builders (per repo Key Conventions)
- The handler should extract the SBOM ID from the path, call `SbomService::advisory_summary`, and return the result as JSON
- Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `AdvisorySeveritySummary` JSON
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response includes 5-minute cache headers
- [ ] Endpoint is registered in the SBOM route tree

## Test Requirements
- [ ] Test successful response with valid SBOM ID
- [ ] Test 404 response for non-existent SBOM
- [ ] Test response body matches `AdvisorySeveritySummary` JSON shape
- [ ] Test cache headers are present in response

## Dependencies
- Depends on: Task 1 — Advisory severity summary model
- Depends on: Task 2 — Advisory summary aggregation service
