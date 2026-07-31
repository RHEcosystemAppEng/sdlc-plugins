## Repository
trustify-backend

## Target Branch
main

## Priority
Major

## Fix Versions
RHTPA 1.5.0

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that returns a license compliance report for the specified SBOM. The endpoint calls the license report service to generate the report and returns the result as JSON.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler function for `GET /api/v2/sbom/{id}/license-report` that extracts the SBOM ID path parameter, calls `LicenseReportService`, and returns the `LicenseReport` as a JSON response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new license report route alongside existing SBOM routes (`/api/v2/sbom/{id}/license-report`)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the given SBOM, with packages grouped by license type and compliance flags based on the configured license policy. Response body: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`

## Implementation Notes
Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`). The handler should:

1. Extract the SBOM ID from the path using `axum::extract::Path`
2. Inject the `LicenseReportService` via Axum state or extension
3. Call the service to generate the report
4. Return `Result<Json<LicenseReport>, AppError>` to match the standard error handling pattern

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing pattern where `list.rs` and `get.rs` routes are registered. Add the new route as `.route("/api/v2/sbom/:id/license-report", get(license_report::handler))`.

Per CONVENTIONS.md §Endpoint registration: register the new route in the module's `endpoints/mod.rs` file following the existing route registration pattern. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` from the handler for consistent error responses. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Reference for path parameter extraction and handler structure for SBOM-scoped endpoints
- `common/src/error.rs::AppError` — Standard error type implementing `IntoResponse` for Axum handlers

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON license report
- [ ] Invalid or missing SBOM ID returns 404 with appropriate error message
- [ ] Response Content-Type is `application/json`
- [ ] Endpoint is registered and reachable via the Axum router
- [ ] OpenAPI schema is generated for the endpoint via `utoipa` annotations

## Test Requirements
- [ ] Handler unit test with a mock service returning a known report
- [ ] Test that an invalid SBOM ID path parameter returns 404
- [ ] Test that the response body matches the expected JSON schema

## Dependencies
- Depends on: Task 2 — Add license report service
