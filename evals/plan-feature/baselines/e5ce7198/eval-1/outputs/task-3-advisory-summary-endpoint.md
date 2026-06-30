# Task 3: Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Create the HTTP endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` that accepts an SBOM ID path parameter and an optional `?threshold` query parameter, calls the service layer to get aggregated severity counts, and returns the JSON response. Register the route in the SBOM endpoint module and configure 5-minute caching via `tower-http` middleware.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Endpoint handler for the advisory summary route

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/advisory-summary` route

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns aggregated advisory severity counts for the specified SBOM
  - Path parameter: `id` (SBOM identifier)
  - Optional query parameter: `threshold` (severity level filter: `critical`, `high`, `medium`, `low`)
  - Response 200: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
  - Response 404: SBOM not found (consistent with existing SBOM endpoints)

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure. The handler should:

1. Extract the SBOM `id` from the path using Axum's `Path` extractor
2. Extract optional `threshold` from query string using Axum's `Query` extractor (define a query params struct)
3. Call `SbomService::get_advisory_summary(id, threshold)` from the service layer
4. Return `Json<AdvisorySeveritySummary>` on success
5. Return appropriate error responses via `AppError` (404 for missing SBOM)

For route registration, follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` where existing routes like `list.rs` and `get.rs` are mounted.

Configure 5-minute cache using `tower-http` caching middleware on this route, following the caching pattern described in the repo conventions.

Per CONVENTIONS.md §Endpoint registration: register the route in `endpoints/mod.rs` and mount via `server/main.rs`.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping for all error paths.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Caching: use `tower-http` caching middleware for the 5-minute cache configuration on the endpoint route builder.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for handler function signature, Axum extractors, and response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `common/src/error.rs::AppError` — error type implementing `IntoResponse` for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct JSON shape
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Optional `?threshold` query parameter filters severity counts
- [ ] Response includes `Cache-Control` header with 5-minute max-age
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`

## Test Requirements
- [ ] Integration test: valid SBOM returns correct severity counts JSON
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: threshold query parameter returns filtered counts
- [ ] Integration test: response content-type is `application/json`

## Dependencies
- Depends on: Task 2 — Implement advisory severity aggregation service method

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `curl http://localhost:8080/api/v2/sbom/{id}/advisory-summary` — returns severity counts JSON

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:654230c60bdc9679e83c70ba0f7b4be69bbff8a7558af3ea347c3fecf7a7f757
