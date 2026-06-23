## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler and register it in the SBOM route configuration. The handler extracts the SBOM ID path parameter and optional `threshold` query parameter, calls `SbomService::advisory_severity_summary()`, and returns the `AdvisorySeveritySummary` as a JSON response. It handles 404 errors for non-existent SBOMs by propagating the `AppError::NotFound` from the service layer.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Handler function `get_advisory_summary` that extracts path/query params and calls the service method

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `GET /api/v2/sbom/{id}/advisory-summary` route and add `pub mod advisory_summary;`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `AdvisorySeveritySummary` JSON with severity counts for the given SBOM. Optional query parameter `threshold` (values: `critical`, `high`, `medium`, `low`) filters to counts at or above the specified severity.
- Response 200: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- Response 404: SBOM not found (consistent with existing SBOM endpoints)

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`). That handler:
1. Extracts the SBOM ID from the path using Axum's `Path<Uuid>` extractor
2. Calls the corresponding `SbomService` method
3. Returns `Result<Json<T>, AppError>` so errors automatically convert to HTTP responses

For the optional `threshold` query parameter, use Axum's `Query<ThresholdParams>` extractor with a struct:
```rust
#[derive(Deserialize)]
pub struct ThresholdParams {
    pub threshold: Option<String>, // or a dedicated enum
}
```

Route registration in `modules/fundamental/src/sbom/endpoints/mod.rs` should follow the pattern used for existing routes like `GET /api/v2/sbom/{id}` — the module's `configure` or route-builder function adds `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::get_advisory_summary))`.

Per CONVENTIONS.md: all handlers return `Result<T, AppError>` with `.context()` wrapping, and each endpoint has its own file in the `endpoints/` directory.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` endpoint scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for path parameter extraction, service invocation, and response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — error type that implements `IntoResponse` for automatic HTTP status code mapping

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct JSON shape for a valid SBOM
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Optional `?threshold=critical` query parameter filters the response to include only severity levels at or above the threshold
- [ ] Endpoint is registered and accessible via the Axum router
- [ ] Response content-type is `application/json`

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with expected severity counts
- [ ] Integration test: `GET /api/v2/sbom/{nonexistent}/advisory-summary` returns 404
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns filtered counts
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 or ignores invalid threshold

## Dependencies
- Depends on: Task 2 — Advisory severity aggregation service (needs `SbomService::advisory_severity_summary()`)

[sdlc-workflow] Description digest: sha256-md:7e23569a749be10c96040b359c065e2b0e876c21efcc1a8c55a183b2ee3fe406
