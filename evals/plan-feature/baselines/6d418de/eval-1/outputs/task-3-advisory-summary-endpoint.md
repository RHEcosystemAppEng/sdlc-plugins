# Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching

## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that serves aggregated advisory severity counts for a given SBOM. The endpoint validates the SBOM exists, calls `SbomService::advisory_summary`, returns the `AdvisorySeveritySummary` as JSON, and is configured with a 5-minute `tower-http` cache. Register the new route in the SBOM endpoints module following existing patterns.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 OK, or 404 if SBOM not found. Response is cached for 5 minutes via `tower-http` caching middleware.

## Implementation Notes
- Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`). Key elements:
  - Extract the SBOM ID from the path using Axum's `Path` extractor
  - Obtain the database connection from application state
  - Call the service method and return `Result<Json<AdvisorySeveritySummary>, AppError>`
  - Use `.context()` wrapping on errors per the project's error handling convention
- For route registration, follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` where existing routes (`list.rs`, `get.rs`) are registered. Add the new route as `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary))`.
- For the 5-minute cache, apply `tower-http` caching middleware on this route. The project uses `tower-http` caching middleware configured in endpoint route builders (see Key Conventions in repo structure). Set `Cache-Control: max-age=300` (5 minutes = 300 seconds).
- Annotate the handler with `utoipa` attributes for OpenAPI spec generation, following the pattern of sibling endpoint handlers.
- Per docs/constraints.md Section 2 (Commit Rules): every commit must reference TC-9001, follow Conventional Commits, and include the AI assistance trailer.
- Per docs/constraints.md Section 3 (PR Rules): the branch must be named after the Jira issue ID; after opening a PR, post its link on the Jira task.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the path parameter extraction, service call, and JSON response pattern for a single-SBOM endpoint
- `modules/fundamental/src/sbom/endpoints/mod.rs` — shows route registration pattern and how to add new routes to the SBOM module
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates list endpoint patterns including error handling
- `common/src/error.rs::AppError` — the error type implementing `IntoResponse` for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` for a valid SBOM
- [ ] Endpoint returns 404 when SBOM ID does not exist, consistent with existing SBOM endpoints
- [ ] Response includes `Cache-Control: max-age=300` header (5-minute cache)
- [ ] Route is registered in the SBOM endpoints module
- [ ] Endpoint appears in the generated OpenAPI spec

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct severity counts for an SBOM with linked advisories
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for a non-existent SBOM ID
- [ ] Integration test: response body matches expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Integration test: verify `Cache-Control` header is present on the response

## Verification Commands
- `cargo build` — full project compiles
- `cargo test --test api` — integration tests pass

## Documentation Updates
- `README.md` — add the new endpoint to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model
- Depends on: Task 2 — Add advisory severity aggregation service method
