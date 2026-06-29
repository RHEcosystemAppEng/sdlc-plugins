# Task 3: Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Repository

trustify-backend

## Target Branch

main

## Description

Wire up a new Axum handler for `GET /api/v2/sbom/{id}/advisory-summary` that calls `SbomService::advisory_summary`, returns the result as JSON, and applies 5-minute caching using the existing tower-http caching middleware. Register the route in the SBOM endpoint module.

## Files to Create

- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function for the advisory-summary endpoint

## Files to Modify

- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new route under `/api/v2/sbom/{id}/advisory-summary` and add `mod advisory_summary;`

## API Changes

- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `AdvisorySeveritySummary` JSON with severity counts for the specified SBOM. Returns 404 if SBOM not found. Cached for 5 minutes.

## Implementation Notes

- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — match the function signature (extractors for path params, State for service), return type (`Result<Json<T>, AppError>`), and error mapping.
- Follow the route registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — add the new route using the same router builder chain.
- Apply 5-minute caching using the existing tower-http caching middleware already used by other endpoints in the codebase. Reference how caching is configured on other GET endpoints.
- Add OpenAPI documentation attributes (`#[utoipa::path(...)]`) following the pattern of existing endpoint handlers to ensure the endpoint appears in generated API docs.
- Extract the SBOM `id` from the path using Axum's `Path<Uuid>` extractor.
- Inject `SbomService` via Axum's `State` extractor (or `Extension`, whichever pattern the codebase uses).
- Per CONVENTIONS.md §Endpoint registration: register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the established route mounting pattern. See the existing routes in that file for the convention.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Error handling: return `Result<Json<AdvisorySeveritySummary>, AppError>` and use `.context()` wrapping for error propagation.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler file scope.
- Per CONVENTIONS.md §Caching: apply tower-http caching middleware with 5-minute max-age on the new route.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

## Reuse Candidates

- `modules/fundamental/src/sbom/endpoints/get.rs` — Handler pattern, extractor usage, error response mapping
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern and router builder chain
- `common/src/error.rs::AppError` — Error handling and HTTP status code mapping

## Acceptance Criteria

- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `AdvisorySeveritySummary` JSON for a valid SBOM
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Response is cached for 5 minutes using existing tower-http cache infrastructure
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] OpenAPI documentation attributes are present on the handler
- [ ] Handler compiles and is wired correctly

## Test Requirements

- [ ] Integration test: verify 200 response with correct JSON shape
- [ ] Integration test: verify 404 for non-existent SBOM ID
- [ ] Integration test: verify cache headers are present in the response

## Dependencies

- Depends on: Task 1 — Add AdvisorySeveritySummary response model
- Depends on: Task 2 — Add advisory summary aggregation to SbomService

## Verification Commands

- `cargo check -p trustify-module-fundamental` — verify compilation
- `cargo test -p trustify-module-fundamental -- sbom::endpoints` — run endpoint tests

## Documentation Updates

- REST API reference documentation — document the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, including path parameters, response schema, caching behavior, and error responses
