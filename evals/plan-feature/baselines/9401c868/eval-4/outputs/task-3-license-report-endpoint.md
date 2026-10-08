## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that returns a license compliance report for the specified SBOM. The endpoint loads the license policy configuration, invokes the license report service, and returns the grouped compliance report as a JSON response.

This completes the API surface for the license compliance report feature (TC-9004), making the report accessible to compliance officers and CI/CD pipelines.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- Axum handler function `get_license_report` that: (1) extracts the SBOM ID from the path parameter, (2) loads the `LicensePolicy` from the config file, (3) calls `LicenseReportService::generate_report()`, (4) returns the `ComplianceReport` as a JSON response with appropriate status codes

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Add `mod license_report;` and register the `GET /api/v2/sbom/{id}/license-report` route in the router alongside existing SBOM routes (`list.rs`, `get.rs`)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: Returns a license compliance report for the given SBOM. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`. Returns 200 on success, 404 if the SBOM ID does not exist, 500 if the license policy file cannot be loaded.

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs`: the handler extracts path parameters using Axum extractors, calls the service layer, and returns `Result<Json<T>, AppError>`.
- Route registration follows the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs`: add a `.route("/api/v2/sbom/:id/license-report", get(license_report::get_license_report))` call to the existing router builder.
- The handler should load the license policy once (consider caching or loading at startup via shared application state rather than reading the file on every request for performance). If file-per-request loading is used initially, add a TODO comment for future optimization.
- Error responses should use the `AppError` enum from `common/src/error.rs` to maintain consistent error response shapes across all endpoints.
- Per CONVENTIONS.md: endpoint handlers return `Result<T, AppError>` with `.context()` wrapping for error propagation.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md: each module's `endpoints/mod.rs` registers routes; follow the existing registration pattern.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint registration scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- Demonstrates the endpoint handler pattern: path parameter extraction, service invocation, JSON response return, and error handling for the SBOM domain
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Shows the route registration pattern for SBOM endpoints; the new route will be added alongside existing routes
- `common/src/error.rs::AppError` -- Error enum implementing `IntoResponse` for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid `ComplianceReport` JSON response for an existing SBOM with license data
- [ ] Response JSON matches the contract: `{ groups: [{ license: string, packages: [...], compliant: boolean }] }`
- [ ] Returns 404 with an appropriate error when the SBOM ID does not exist
- [ ] Returns an error response when the license policy configuration file is missing or malformed
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs` and accessible via the Axum router

## Test Requirements
- [ ] Handler test: returns 200 with grouped license data for a valid SBOM
- [ ] Handler test: returns 404 for a non-existent SBOM ID
- [ ] Handler test: response JSON structure matches the documented contract
- [ ] Handler test: non-compliant licenses are correctly flagged in the response

## Verification Commands
- `cargo build` -- Compiles without errors after adding the new endpoint
- `cargo test` -- All existing tests continue to pass

## Documentation Updates
- `README.md` -- Add the new `/api/v2/sbom/{id}/license-report` endpoint to the API reference if one exists

## Dependencies
- Depends on: Task 2 -- Add license compliance report service with transitive dependency resolution
