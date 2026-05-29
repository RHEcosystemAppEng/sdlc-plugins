## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that returns aggregated advisory severity counts for a given SBOM. This endpoint supports an optional `?threshold=critical|high|medium|low` query parameter to filter counts to only severities at or above the specified threshold. The endpoint includes 5-minute response caching using the existing `tower-http` caching middleware.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`. Optional query param `?threshold=critical|high|medium|low` filters to severities at or above threshold.
- Returns 404 if SBOM ID does not exist (consistent with existing SBOM endpoints)

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (GET handler for SBOM details) and `modules/fundamental/src/sbom/endpoints/list.rs` (GET handler for SBOM list). Both use Axum extractors (`Path`, `Query`, `State`) and return `Result<Json<T>, AppError>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing SBOM routes. Follow the route registration pattern used for `list.rs` and `get.rs`.
- For the optional `?threshold` query parameter, define a `QueryParams` struct with `threshold: Option<SeverityThreshold>` and derive `Deserialize`. Parse threshold values as an enum: `critical`, `high`, `medium`, `low`.
- When threshold is provided, zero out severity counts below the threshold level and recalculate `total` accordingly.
- Add 5-minute cache control headers using the existing `tower-http` caching middleware pattern. Reference the cache configuration in endpoint route builders documented in the repository conventions.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per the error handling convention in `common/src/error.rs`.
- Per docs/constraints.md §3.1: the feature branch must be named after the Jira issue ID.
- Per docs/constraints.md §2.1-2.3: commits must reference the Jira issue ID, follow Conventional Commits, and include the AI attribution trailer.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — GET handler for SBOM details; follow its Axum extractor usage, error handling, and response pattern.
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration module; follow its pattern for adding new routes.
- `common/src/error.rs::AppError` — error handling enum; use for 404 responses consistent with existing SBOM endpoints.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with `critical`, `high`, `medium`, `low`, `total` fields
- [ ] Endpoint returns 404 with appropriate error when SBOM ID does not exist
- [ ] Optional `?threshold` query parameter filters severity counts to at-or-above the specified level
- [ ] Response includes cache control headers for 5-minute caching
- [ ] Route is registered in the SBOM endpoints module

## Test Requirements
- [ ] Integration test: GET with valid SBOM ID returns 200 with correct severity counts
- [ ] Integration test: GET with non-existent SBOM ID returns 404
- [ ] Integration test: GET with `?threshold=critical` returns only critical count (others zeroed) with recalculated total
- [ ] Integration test: GET with `?threshold=high` returns critical and high counts, medium and low zeroed
- [ ] Integration test: GET without threshold returns all severity counts
- [ ] Integration test: response includes appropriate cache control headers

## Verification Commands
- `cargo test --test api advisory_summary` — all advisory summary endpoint tests pass
- `cargo clippy -- -D warnings` — no warnings in new code

## Documentation Updates
- `README.md` — add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint to the API reference section, including path, query parameters, response shape, and error codes

## Dependencies
- Depends on: Task 2 — Add advisory severity aggregation service method

[sdlc-workflow] Description digest: sha256:5b823fbe968c5d5d588faed2fe42cdcc523904be52b55bc0ba590aef69d2d5f0
