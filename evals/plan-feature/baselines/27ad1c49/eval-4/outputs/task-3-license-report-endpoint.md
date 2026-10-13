## Repository
trustify-backend

## Target Branch
main

## Description
Add the GET /api/v2/sbom/{id}/license-report endpoint that exposes the license compliance report service to API consumers. Register the route in the SBOM endpoints module so it is mounted alongside existing SBOM routes.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new license-report route alongside existing routes (list, get)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — implement the Axum handler for GET /api/v2/sbom/{id}/license-report: extract SBOM ID from path, load license policy, call the service, return JSON response

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a LicenseComplianceReport JSON response with grouped license data and compliance flags

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction and response formatting.
- Follow the route registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` for adding the new route.
- The handler should extract the SBOM ID from the path, load the LicensePolicy from the configured JSON file path (consider making the path configurable via application state or environment), call the license report service method, and return the LicenseComplianceReport as JSON.
- Use `Result<Json<LicenseComplianceReport>, AppError>` as the return type, consistent with existing endpoint handlers.
- Return 404 if the SBOM ID does not exist (propagated from the service layer's AppError).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for path parameter extraction pattern (`Path(id): Path<Uuid>`)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `common/src/error.rs::AppError` — error type that implements IntoResponse for automatic HTTP error responses

## Acceptance Criteria
- [ ] GET /api/v2/sbom/{id}/license-report returns 200 with LicenseComplianceReport JSON
- [ ] Response body matches format: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`
- [ ] Returns 404 when SBOM ID does not exist
- [ ] Route is registered in the SBOM endpoints module
- [ ] No authentication bypass — endpoint uses the same auth middleware as other SBOM endpoints

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo check -p trustify-server` — full server compiles with new route mounted

## Dependencies
- Depends on: Task 2 — Implement license compliance report service
