# Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }

## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint calls `SbomService::advisory_summary`, applies a 5-minute cache via `tower-http` caching middleware, and returns 404 for non-existent SBOMs. This is the primary deliverable of TC-9001.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function for the advisory summary endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route and add `pub mod advisory_summary;`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with `Content-Type: application/json`. Returns 404 if the SBOM ID does not exist. Response is cached for 5 minutes.

## Implementation Notes
Create the handler function following the pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (the existing `GET /api/v2/sbom/{id}` handler). The handler should:

1. Extract the SBOM ID from the path parameter (using Axum's `Path` extractor).
2. Call `SbomService::advisory_summary(id, &db)`.
3. On success, return `Json(summary)` with HTTP 200.
4. On not-found error, return HTTP 404 (the `AppError` conversion in `common/src/error.rs` should handle this automatically via `IntoResponse`).

For caching, apply `tower-http` cache control headers or middleware with a 5-minute max-age. Reference the existing caching patterns described in the Key Conventions — cache configuration is done in endpoint route builders.

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing routes for `/api/v2/sbom`. Follow the same registration pattern used for `list.rs` and `get.rs`.

Per CONVENTIONS.md §Error handling: the handler must return `Result<Json<AdvisorySeveritySummary>, AppError>` and use `.context()` for error wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` error-handling scope.

Per CONVENTIONS.md §Endpoint registration: register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` and ensure it is mounted via `server/main.rs`.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

Per CONVENTIONS.md §Caching: apply `tower-http` caching middleware with a 5-minute TTL in the route builder.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's caching scope.

Per CONVENTIONS.md §Framework: use Axum extractors (`Path`, `State`) and return types (`Json`) for the handler.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Axum framework scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM detail endpoint; follow its handler signature, extractor usage, and error handling pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow for adding the new route
- `common/src/error.rs::AppError` — automatic `IntoResponse` conversion for error types
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::advisory_summary` — the service method created in Task 2

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns HTTP 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Endpoint returns HTTP 404 when the SBOM ID does not exist
- [ ] Response includes cache-control headers with a 5-minute (300s) max-age
- [ ] Endpoint is registered and reachable when the server starts
- [ ] OpenAPI schema includes the new endpoint (via `utoipa` annotations)

## Test Requirements
- [ ] Integration test: valid SBOM ID returns 200 with correct JSON shape
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Verify cache headers are present in the response

## Verification Commands
- `cargo build` — ensure the project compiles with the new endpoint
- `cargo test` — all existing and new tests pass
- `curl http://localhost:8080/api/v2/sbom/{id}/advisory-summary` — returns expected JSON (manual smoke test)

## Dependencies
- Depends on: Task 2 — Implement advisory severity aggregation query in SbomService
