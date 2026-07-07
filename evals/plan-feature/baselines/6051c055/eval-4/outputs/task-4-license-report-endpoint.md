## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `GET /api/v2/sbom/{id}/license-report` endpoint that returns a license compliance report for the specified SBOM. The endpoint delegates to `LicenseReportService::generate_report` and returns the `LicenseReport` as a JSON response. It also registers the route in the SBOM endpoint router.

## Files to Modify
- `modules/fundamental/src/license_report/mod.rs` -- add `pub mod endpoints;` to expose the endpoints submodule
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the license report route under the SBOM path prefix by nesting the license report router

## Files to Create
- `modules/fundamental/src/license_report/endpoints.rs` -- Axum handler function and route configuration

## Implementation Notes
- Follow the endpoint pattern from `modules/fundamental/src/sbom/endpoints/mod.rs` for handler structure and route registration
- Handler signature: `async fn get_license_report(Path(sbom_id): Path<Uuid>, State(db): State<DatabaseConnection>) -> Result<Json<LicenseReport>, AppError>`
- Add `#[utoipa::path]` attribute macro for OpenAPI documentation:
  - Tag: "sbom"
  - Path: "/api/v2/sbom/{id}/license-report"
  - Response: 200 with `LicenseReport` schema, 404 for SBOM not found
- Register the route via `.route("/api/v2/sbom/:id/license-report", get(get_license_report))` in the SBOM router in `modules/fundamental/src/sbom/endpoints/mod.rs`
- Ensure the endpoint is behind the same authentication/authorization middleware as other SBOM endpoints
- Use existing `AppError` mapping to HTTP status codes from `common/src/error.rs`
- Per CONVENTIONS.md Key Conventions (Error handling): the handler must return `Result<Json<LicenseReport>, AppError>` with `.context()` wrapping on all fallible operations.
  Applies: task creates `modules/fundamental/src/license_report/endpoints.rs` matching the convention's Rust file scope.
- Per CONVENTIONS.md Key Conventions (Endpoint registration): register the route in `endpoints/mod.rs` following the existing pattern for /api/v2/sbom routes.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint registration scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- reference for handler function pattern, Path extraction, and error response
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- reference for route registration pattern

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid `LicenseReport` JSON body
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Response Content-Type is `application/json`
- [ ] Endpoint appears in the OpenAPI specification under the "sbom" tag
- [ ] Route is protected by the same auth middleware as other SBOM endpoints
- [ ] Invalid SBOM ID format returns 400

## Test Requirements
- [ ] Integration test: valid SBOM returns 200 with correct report structure
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: invalid UUID format returns 400
- [ ] Integration test: unauthenticated request returns 401 (if auth is enabled)

## Dependencies
- Depends on: Task 3 -- Add license report service
