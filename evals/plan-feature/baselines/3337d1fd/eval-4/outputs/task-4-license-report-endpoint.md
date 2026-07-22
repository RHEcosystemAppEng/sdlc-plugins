## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that exposes the license compliance report service to API consumers. This endpoint loads the license policy configuration, invokes the report service, and returns the structured compliance report as JSON.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new license-report route under the existing `/api/v2/sbom` router
- `server/src/main.rs` — No changes expected if SBOM routes are already mounted (verify)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Handler function `get_license_report(Path(id): Path<Uuid>, State(state): State<AppState>) -> Result<Json<LicenseReportResponse>, AppError>`. Loads the `LicensePolicy` from the configured path, calls `LicenseReportService::generate_report()`, returns `Json(report)`. Includes `#[utoipa::path(...)]` annotation for OpenAPI documentation.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure and Axum extractors.
- Register the route as `.route("/api/v2/sbom/:id/license-report", get(get_license_report))` in `endpoints/mod.rs`, following the existing route registration pattern.
- The license policy file path should be read from application state or environment variable, not hardcoded.
- Return `StatusCode::NOT_FOUND` (via `AppError`) if the SBOM does not exist.
- Return `StatusCode::INTERNAL_SERVER_ERROR` if the license policy file cannot be loaded.
- Consider caching the loaded `LicensePolicy` in application state to avoid re-reading from disk on every request.
- Add the `#[utoipa::path]` macro for OpenAPI spec generation, documenting the endpoint parameters and response schema.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid `LicenseReportResponse` JSON body
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Returns 500 with a meaningful error when the license policy file is missing
- [ ] Endpoint is documented in the OpenAPI spec
- [ ] Route is accessible through the existing authentication middleware

## Test Requirements
- [ ] Integration test: call the endpoint with a valid SBOM ID and verify 200 response with correct JSON structure
- [ ] Integration test: call the endpoint with a non-existent SBOM ID and verify 404 response
- [ ] Integration test: verify response includes both direct and transitive dependency licenses

## Dependencies
- Depends on: Task 3 — License report service (provides the core report generation logic)
