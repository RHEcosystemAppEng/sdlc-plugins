## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint handler for `GET /api/v2/sbom/{id}/license-report` and register it in the SBOM route configuration. The handler extracts the SBOM ID from the path, invokes the license report service, and returns the report as a JSON response.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler function that extracts the SBOM ID path parameter, calls `LicenseReportService::generate_report()`, and returns `Json<LicenseReport>`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `pub mod license_report;` and register the `GET /api/v2/sbom/{id}/license-report` route alongside existing SBOM routes (following the pattern used for `list.rs` and `get.rs`)

## Implementation Notes
- Follow the endpoint pattern from `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction and response handling
- The handler signature should accept Axum extractors: `Path(id)` for the SBOM ID and `State(app_state)` for access to the database connection and services
- Return `Result<Json<LicenseReport>, AppError>` consistent with other handlers in the codebase
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` where existing routes like `/api/v2/sbom` (list) and `/api/v2/sbom/{id}` (get) are registered
- No changes to `server/src/main.rs` are needed since the SBOM module routes are already mounted there
- Consider adding `Cache-Control` headers via `tower-http` caching middleware, consistent with the caching approach noted in the repository conventions

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns a 200 response with a JSON `LicenseReport` body
- [ ] Invalid or non-existent SBOM IDs return a 404 response with a meaningful error message
- [ ] Response content type is `application/json`
- [ ] Route is properly registered and accessible without changes to server/main.rs

## Test Requirements
- [ ] Verify the route is registered by checking it responds to GET requests
- [ ] Verify path parameter extraction works for valid SBOM IDs

## Dependencies
- Depends on: Task 3 — Implement license report service

## Digest
[sdlc-workflow] Description digest: sha256-md:08b4b10ca04096050aa2b885ef6eb5ddd7b6a2f897022745ef70567dbe53ef5e
