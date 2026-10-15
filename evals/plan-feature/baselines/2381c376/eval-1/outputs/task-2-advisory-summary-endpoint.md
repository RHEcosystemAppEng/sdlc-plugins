## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the `SbomService::advisory_severity_summary` method (added in Task 1), applies an optional `?threshold` query parameter to filter counts above a severity level, and caches responses for 5 minutes using `tower-http` caching middleware. Returns 404 if the SBOM ID does not exist, consistent with existing SBOM endpoints.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` with threshold query param support and 5-minute cache configuration

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `advisory_summary` route under the `/api/v2/sbom/{id}` path prefix

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with optional `?threshold=critical|high|medium|low` query param to filter counts above the specified severity level. Returns 404 if SBOM ID does not exist.

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction, service injection, and error response handling.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing `get` and `list` routes, following the same route builder pattern.
- For caching, use `tower-http` caching middleware with a 5-minute max-age, following the caching pattern described in the endpoint route builders. Apply the cache layer to the advisory-summary route definition.
- For the `?threshold` query parameter, define a `ThresholdQuery` struct with an `Option<String>` field. When present, filter the `AdvisorySeveritySummary` to only include counts at or above the specified severity level (Critical > High > Medium > Low). This is a non-MVP feature but should be implemented as part of the endpoint.
- The handler should be `async fn advisory_summary(Path(id): Path<Uuid>, Query(params): Query<ThresholdQuery>, service: ...) -> Result<Json<AdvisorySeveritySummary>, AppError>`.
- Per CONVENTIONS.md §Module Pattern: follow the `endpoints/` structure for new endpoint handlers.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoints directory scope.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md §Endpoint Registration: register routes in the module's `endpoints/mod.rs`; `server/main.rs` mounts all modules.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Caching: use `tower-http` caching middleware with cache configuration in endpoint route builders.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler for SBOM details; follow its pattern for path extraction, service injection, and error mapping
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration; follow the router builder pattern for adding the new route

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Response is cached for 5 minutes (cache-control header set)
- [ ] `?threshold=critical` returns only the critical count and total
- [ ] `?threshold=high` returns critical and high counts and total
- [ ] `?threshold=medium` returns critical, high, and medium counts and total
- [ ] `?threshold=low` returns all counts (equivalent to no threshold)
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`

## Test Requirements
- [ ] Handler returns correct JSON shape for a valid SBOM with advisories
- [ ] Handler returns 404 for a nonexistent SBOM ID
- [ ] Cache-control header includes `max-age=300`
- [ ] Threshold filtering works correctly for each severity level

## Verification Commands
- `cargo test --test api -- advisory_summary` — integration tests pass
- `curl http://localhost:8080/api/v2/sbom/{id}/advisory-summary` — returns expected JSON shape

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
