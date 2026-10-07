## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that returns a license compliance report for a given SBOM. The endpoint uses the LicenseReportService to generate the report and returns the result as a JSON response. This task also registers the new route in the SBOM endpoint module and ensures it is mounted by the server.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- Axum handler function `get_license_report(Path(id): Path<Uuid>, State(service): State<...>, State(policy): State<...>) -> Result<Json<LicenseReport>, AppError>` that delegates to LicenseReportService

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the `GET /api/v2/sbom/{id}/license-report` route in the SBOM router, add `pub mod license_report;`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: returns a license compliance report grouped by license type with compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [{ name: "...", version: "..." }], compliant: true }] }`

## Implementation Notes
- The handler should extract the SBOM ID from the path, load the license policy (from application state or config), call `LicenseReportService::generate_report()`, and return the result as `Json<LicenseReport>`.
- Per CONVENTIONS.md $Error Handling: the handler must return `Result<Json<LicenseReport>, AppError>` and wrap errors with `.context()`.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust endpoint file scope.
  See `modules/fundamental/src/sbom/endpoints/get.rs` for the established handler error pattern.
- Per CONVENTIONS.md $Endpoint Registration: register the route in `endpoints/mod.rs` following the existing pattern for GET routes.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration file scope.
  See `modules/fundamental/src/sbom/endpoints/mod.rs` for the established route registration pattern (`.route("/{id}", get(get::get_sbom))`).
- Per CONVENTIONS.md $Caching: consider adding tower-http caching middleware configuration to the route builder if the report data is cache-friendly.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust endpoint file scope.
  See `modules/fundamental/src/sbom/endpoints/mod.rs` for existing cache configuration patterns.
- If `server/src/main.rs` already mounts all SBOM routes via the SBOM module's router, no changes are needed there. Verify by inspecting the existing mount pattern.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs::get_sbom` -- existing GET handler for /api/v2/sbom/{id}; follow its pattern for path extraction, state access, service delegation, and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- existing route registration; follow its Router builder pattern for adding the new route
- `common/src/error.rs::AppError` -- shared error type; use for handler return type

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON body containing license groups
- [ ] Each group in the response contains `license` (string), `packages` (array), and `compliant` (boolean) fields
- [ ] The endpoint returns 404 when the SBOM ID does not exist
- [ ] The endpoint returns a proper error response for invalid SBOM ID formats
- [ ] The route is registered and accessible via the SBOM router

## Test Requirements
- [ ] Handler returns 200 with correctly structured LicenseReport for a valid SBOM ID
- [ ] Handler returns 404 for a non-existent SBOM ID
- [ ] Response JSON shape matches the documented API contract

## Verification Commands
- `cargo build -p trustify-module-fundamental` -- builds without errors
- `cargo build -p trustify-server` -- server builds with new route registered

## Dependencies
- Depends on: Task 2 -- Add license report service with dependency tree walking
