# Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching

## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the `SbomService::advisory_summary` method (Task 1) and returns the `AdvisorySeveritySummary` as JSON. Configure a 5-minute `tower-http` cache on the endpoint. Add support for the optional `?threshold` query parameter that filters counts to only include severities at or above the specified level.

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with 5-minute cache
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: optional severity threshold filter (non-MVP)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` with threshold query parameter support and cache configuration

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/advisory-summary` route under the existing `/api/v2/sbom/{id}` path, add `pub mod advisory_summary;`

## Implementation Notes
- Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — the handler extracts the SBOM ID from the path, calls the service method, and returns the result as JSON.
- Use Axum's `Path` extractor for the SBOM ID and `Query` extractor for the optional `threshold` parameter.
- Define a `ThresholdQuery` struct with `threshold: Option<String>` for the query parameter. Valid values: `"critical"`, `"high"`, `"medium"`, `"low"`. If present, zero out counts below the threshold severity and recalculate `total`.
- Configure `tower-http` caching middleware on the route with a 5-minute (300-second) TTL. Reference existing cache configuration in endpoint route builders per the project's caching convention.
- The handler should return `Result<Json<AdvisorySeveritySummary>, AppError>` following the project's error handling pattern.
- Per Key Conventions §Endpoint registration: register the route in `endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` file scope.
- Per Key Conventions §Caching: use `tower-http` caching middleware for the 5-minute cache TTL, following the cache configuration pattern in endpoint route builders.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` file scope.
- Per Key Conventions §Error handling: handler returns `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET endpoint handler; follow the same pattern for path extraction, service invocation, and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern; follow for adding the new route
- `common/src/error.rs::AppError` — error type for handler return values

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ critical, high, medium, low, total }`
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response is cached for 5 minutes via `tower-http` caching
- [ ] Optional `?threshold` query parameter filters severity counts (zeroes out levels below threshold and recalculates total)
- [ ] Invalid threshold values return 400 Bad Request
- [ ] Route is registered under the existing SBOM path group

## Test Requirements
- [ ] Integration test: endpoint returns correct severity counts for a known SBOM
- [ ] Integration test: endpoint returns 404 for nonexistent SBOM ID
- [ ] Integration test: `?threshold=critical` returns only critical count (other levels zeroed)
- [ ] Integration test: `?threshold=high` returns critical and high counts
- [ ] Integration test: invalid `?threshold` value returns 400
- [ ] Integration test: response content-type is `application/json`

## Verification Commands
- `cargo test --test api -- advisory_summary` — run integration tests for the new endpoint

## Documentation Updates
- `docs/api/` or OpenAPI spec — add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with request parameters and response schema

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
