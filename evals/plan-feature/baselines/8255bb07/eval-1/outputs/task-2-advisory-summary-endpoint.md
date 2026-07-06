## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns advisory severity counts for a given SBOM. The endpoint calls the SbomService aggregation method (from Task 1) and returns the AdvisorySeveritySummary response. It includes a 5-minute response cache using tower-http caching middleware and supports an optional `?threshold` query parameter to filter counts to only severities at or above the specified level.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler for GET /api/v2/sbom/{id}/advisory-summary with threshold query parameter parsing and 5-minute cache configuration

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the advisory-summary route under /api/v2/sbom/{id}/advisory-summary
- `tests/api/sbom.rs` — add integration tests for the advisory-summary endpoint

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: returns counts filtered to severities at or above the specified threshold

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/`: see `get.rs` (GET /api/v2/sbom/{id}) for the handler structure, path parameter extraction, and error response pattern.
- The handler function signature should follow the Axum extractor pattern: `async fn get_advisory_summary(Path(id): Path<Uuid>, Query(params): Query<ThresholdParams>, State(service): State<SbomService>) -> Result<Json<AdvisorySeveritySummary>, AppError>`.
- Define a `ThresholdParams` struct with `threshold: Option<String>` for the query parameter. Valid values: "critical", "high", "medium", "low". When present, zero out counts for severities below the threshold and recalculate total.
- Configure 5-minute cache using tower-http caching middleware. Reference the existing caching patterns in the endpoint route builders as noted in Key Conventions.
- Register the route in `endpoints/mod.rs` following the existing pattern where `list.rs` and `get.rs` are registered. Add `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::get_advisory_summary))`.
- Integration tests should follow the pattern in `tests/api/sbom.rs`: set up test data, call the endpoint, assert on status code and response body.
- Per Key Conventions — Endpoint registration: each module's `endpoints/mod.rs` registers routes.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per Key Conventions — Caching: use tower-http caching middleware with cache configuration in endpoint route builders.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint file scope.
- Per Key Conventions — Testing: integration tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/sbom.rs` matching the convention's test file scope.
- Per Key Conventions — Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the handler pattern for GET /api/v2/sbom/{id} including path parameter extraction, service call, and error response; follow this pattern for the advisory-summary handler
- `modules/fundamental/src/sbom/endpoints/mod.rs` — shows route registration pattern to follow
- `tests/api/sbom.rs` — existing SBOM integration test patterns to follow for the new endpoint tests
- `common/src/model/paginated.rs::PaginatedResults` — reference for response wrapper patterns, though this endpoint uses a simple struct response

## Acceptance Criteria
- [ ] GET /api/v2/sbom/{id}/advisory-summary returns 200 with `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` for a valid SBOM
- [ ] GET /api/v2/sbom/{id}/advisory-summary returns 404 for a non-existent SBOM ID
- [ ] Response is cached for 5 minutes (Cache-Control header present)
- [ ] GET /api/v2/sbom/{id}/advisory-summary?threshold=critical returns only critical count (other severities zeroed, total reflects filtered count)
- [ ] GET /api/v2/sbom/{id}/advisory-summary?threshold=high returns critical and high counts (medium and low zeroed)
- [ ] Invalid threshold values return 400 Bad Request

## Test Requirements
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary with valid SBOM returns 200 and correct severity counts
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary with non-existent SBOM returns 404
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary?threshold=critical returns filtered counts
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary?threshold=high returns critical and high counts only
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary with invalid threshold returns 400
- [ ] Integration test: verify response includes appropriate Cache-Control header

## Verification Commands
- `cargo test --test api sbom::advisory_summary` — run advisory-summary integration tests, expect all pass

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
