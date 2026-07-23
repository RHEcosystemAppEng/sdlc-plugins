# Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that returns the license compliance report for a given SBOM. The endpoint calls the `LicenseReportService` (Task 2) to generate the report and returns the `LicenseReport` as a JSON response.

This endpoint enables compliance teams and CI/CD pipelines to retrieve a structured license audit with compliance flags in a single API call.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report`; extracts SBOM ID from path, loads license policy, calls `LicenseReportService::generate()`, returns `LicenseReport` as JSON

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/license-report` route under the existing `/api/v2/sbom/{id}` path; add the `license_report` module declaration

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a `LicenseReport` JSON response containing packages grouped by license with compliance flags. Response shape: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`

## Implementation Notes
- Follow the established endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for the handler structure: extract path parameters, call the service, return `Json<LicenseReport>`.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` file scope.
- Per project conventions (§Endpoint registration): register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for existing SBOM routes (e.g., `list.rs`, `get.rs`). The route should be `.route("/{id}/license-report", get(license_report::handler))`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint module scope.
- Per project conventions (§Error handling): the handler must return `Result<Json<LicenseReport>, AppError>` with `.context()` wrapping. See `modules/fundamental/src/sbom/endpoints/get.rs` for the established error handling pattern.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` file scope.
- Per project conventions (§Framework): use Axum extractors (`Path`, `State`) following the same pattern as the existing SBOM `get` handler. The license policy should be loaded from the application state or configuration.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` file scope.
- No caching middleware is needed initially — the report is generated fresh each time. Consider adding `tower-http` cache headers in a follow-up if performance requires it.
- The endpoint does not use `PaginatedResults<T>` since it returns a single report, not a paginated list.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing SBOM GET endpoint handler; follow the same pattern for path parameter extraction and service invocation
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern for adding new SBOM sub-routes
- `common/src/error.rs::AppError` — Error type implementing `IntoResponse` for Axum error handling

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a valid `LicenseReport` JSON for an existing SBOM
- [ ] Returns HTTP 404 with an `AppError` response when the SBOM ID does not exist
- [ ] Response content type is `application/json`
- [ ] Route is registered and accessible at the correct path

## Test Requirements
- [ ] Integration test: GET request returns 200 with correct JSON shape for a valid SBOM
- [ ] Integration test: GET request returns 404 for a non-existent SBOM ID
- [ ] Integration test: verify response groups contain expected license and package data
- [ ] Integration test: verify compliance flags reflect the configured policy

## Verification Commands
- `cargo build -p fundamental` — compiles without errors
- `cargo test -p fundamental` — all tests pass

## Documentation Updates
- `README.md` — Add the new endpoint to the API reference section (if present)

## Dependencies
- Depends on: Task 1 — Add license policy configuration file and loader
- Depends on: Task 2 — Create license report model structs and service with transitive dependency resolution
