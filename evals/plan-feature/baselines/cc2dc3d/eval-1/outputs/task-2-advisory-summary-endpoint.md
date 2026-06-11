## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the `SbomService::advisory_severity_summary` method (from Task 1) and returns the `AdvisorySeveritySummary` response. It includes a 5-minute cache via tower-http caching middleware and supports an optional `?threshold` query parameter to filter severity counts above a given threshold level.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for GET /api/v2/sbom/{id}/advisory-summary with threshold query parameter support

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new advisory-summary route alongside existing SBOM routes, add `pub mod advisory_summary;`
- `modules/fundamental/Cargo.toml` — add tower-http cache dependency if not already present

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with 5-minute cache; supports optional `?threshold=critical|high|medium|low` query parameter to filter counts at or above the specified severity level

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` for the handler function signature, path parameter extraction, and error response pattern (`Result<Json<T>, AppError>`).
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern for `/api/v2/sbom/{id}` and `/api/v2/sbom`.
- For caching, use `tower-http` caching middleware with a 5-minute TTL, following the established cache configuration pattern in endpoint route builders as noted in the repository conventions.
- For the optional `?threshold` query parameter (non-MVP but included for completeness): define a `ThresholdQuery` struct with `#[serde(default)]` and extract it via Axum's `Query<ThresholdQuery>`. When threshold is set, filter the response to only include severity levels at or above the threshold (e.g., `?threshold=high` returns only critical and high counts, zeroing out medium and low). The threshold values map to a severity ordering: critical > high > medium > low.
- The handler should extract the SBOM ID from the path using Axum's `Path<Uuid>` extractor, consistent with `modules/fundamental/src/sbom/endpoints/get.rs`.
- Use `utoipa::path` attribute macro to document the endpoint for OpenAPI schema generation, following the pattern in sibling endpoint files.
- Per docs/constraints.md section 2 (Commit Rules): commit must reference TC-9001, use Conventional Commits format, and include the Assisted-by trailer.
- Per docs/constraints.md section 3 (PR Rules): branch named after the Jira issue ID, PR link posted to Jira after creation.
- Per docs/constraints.md section 5 (Code Change Rules): changes scoped to listed files, inspect code before modifying, follow referenced patterns.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM endpoint handler showing path parameter extraction, service call, and JSON response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow for adding the new route
- `common/src/error.rs::AppError` — error handling enum for consistent 404 and 500 responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with fields: critical, high, medium, low, total
- [ ] Returns 404 when SBOM ID does not exist
- [ ] Response is cached for 5 minutes via tower-http middleware
- [ ] Optional `?threshold` query parameter filters severity counts above the specified level
- [ ] Endpoint is registered in the SBOM route group and accessible via the API

## Test Requirements
- [ ] Endpoint handler compiles and is registered at the correct route path
- [ ] Integration tests for this endpoint are covered in Task 4

## Verification Commands
- `cargo build -p fundamental` — verify the module compiles without errors
- `cargo clippy -p fundamental` — verify no lint warnings

## Documentation Updates
- `README.md` — add the new endpoint to the API endpoint listing if an endpoint summary exists

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and service method
