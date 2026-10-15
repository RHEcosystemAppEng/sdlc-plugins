## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that invokes the license compliance report service and returns the structured compliance report as JSON. Register the route in the SBOM endpoint module following the established endpoint registration pattern.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- Axum handler function for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the new `/api/v2/sbom/{id}/license-report` route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: returns a `LicenseComplianceReport` JSON response with packages grouped by license and compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern: see `modules/fundamental/src/sbom/endpoints/get.rs` for the `GET /api/v2/sbom/{id}` handler as the structural reference. The new handler should follow the same parameter extraction, service invocation, and response serialization pattern.
- Route registration: add the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs`. The route should be `.route("/api/v2/sbom/:id/license-report", get(license_report))` or equivalent Axum routing syntax.
- The handler extracts the SBOM ID from the path parameter, calls `LicenseReportService::generate_report`, and returns the result as `Json<LicenseComplianceReport>`.
- Error handling: return `Result<Json<LicenseComplianceReport>, AppError>` -- errors from the service layer propagate as HTTP error responses via the existing `AppError` into-response implementation in `common/src/error.rs`.
- This endpoint does not use `PaginatedResults<T>` since it returns a single report, not a paginated list.
- Per docs/constraints.md S5.3: follow the patterns referenced in Implementation Notes (existing endpoint handlers).
- Per docs/constraints.md S4.6: all file paths are real paths from the repository structure.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- reference handler for `GET /api/v2/sbom/{id}` showing path parameter extraction and service call pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- route registration pattern for SBOM endpoints
- `common/src/error.rs::AppError` -- error-to-HTTP-response conversion

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON body matching the `LicenseComplianceReport` schema
- [ ] The response includes packages grouped by license with `compliant` flags
- [ ] A request for a non-existent SBOM ID returns an appropriate HTTP error (404)
- [ ] The route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] The endpoint follows the same error handling pattern as existing SBOM endpoints

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` returns 200 for a valid SBOM with license data
- [ ] Integration test: response JSON structure matches the expected schema (groups array with license, packages, compliant fields)
- [ ] Integration test: `GET /api/v2/sbom/{invalid-id}/license-report` returns 404
- [ ] Integration test: non-compliant licenses are correctly flagged in the response

## Verification Commands
- `cargo test --test api license_report` -- run license report integration tests, expect all pass
- `cargo check -p fundamental` -- verify the fundamental module compiles without errors

## Documentation Updates
- `README.md` -- add the new endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 1 -- Add license compliance report model and policy configuration
- Depends on: Task 2 -- Add license compliance report service with transitive dependency resolution
