## Repository
trustify-backend

## Target Branch
main

## Description
Create the HTTP endpoint handler for `GET /api/v2/sbom/{id}/license-report` and register the route in the SBOM module's endpoint configuration. This endpoint delegates to the LicenseReportService to generate the compliance report and returns the result as a JSON response.

## Files to Create
- `modules/fundamental/src/sbom/license_report/endpoints/mod.rs` — Route registration for the license-report endpoint under the sbom scope
- `modules/fundamental/src/sbom/license_report/endpoints/report.rs` — GET handler: extract SBOM ID from path, call LicenseReportService, return LicenseReport as JSON

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Mount the license-report routes as a nested scope under `/api/v2/sbom/{id}/license-report`
- `modules/fundamental/src/sbom/license_report/mod.rs` — Add `pub mod endpoints;` submodule declaration

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM. Response body: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`

## Implementation Notes
Follow the existing endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` for the handler structure: extract path parameters, call the service, return the result.

The handler should:
1. Extract the SBOM ID from the path using Axum's `Path` extractor
2. Obtain a database connection from the Axum state
3. Call `LicenseReportService::generate_report(db, sbom_id)` 
4. Return the `LicenseReport` serialized as JSON

For route registration, follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` which registers routes for the sbom module. The license-report route should be nested under the existing sbom routes.

For error responses, the handler returns `Result<Json<LicenseReport>, AppError>` following the pattern in `common/src/error.rs` where AppError implements IntoResponse.

Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules. Applies: task creates `modules/fundamental/src/sbom/license_report/endpoints/mod.rs` matching the convention's endpoint registration scope.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/license_report/endpoints/report.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Framework: use Axum for HTTP handling. Applies: task creates `modules/fundamental/src/sbom/license_report/endpoints/report.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing GET handler for SBOM details; follow the same pattern for path extraction and response structure
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow for mounting the new endpoint
- `common/src/error.rs::AppError` — Error type implementing IntoResponse for error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON LicenseReport body for a valid SBOM ID
- [ ] Endpoint returns appropriate error status for non-existent SBOM ID
- [ ] Route is correctly registered and reachable via the Axum router
- [ ] Response content type is application/json
- [ ] Handler follows the existing error handling pattern with `Result<T, AppError>`

## Test Requirements
- [ ] Integration test: GET license-report for a valid SBOM returns 200 with expected group structure
- [ ] Integration test: GET license-report for non-existent SBOM returns appropriate error status
- [ ] Integration test: response contains correct license groupings and compliance flags for known test data

## Documentation Updates
- `README.md` — Add license report endpoint to the API documentation section, including request/response format and license policy configuration instructions

## Dependencies
- Depends on: Task 2 — License report model and service
