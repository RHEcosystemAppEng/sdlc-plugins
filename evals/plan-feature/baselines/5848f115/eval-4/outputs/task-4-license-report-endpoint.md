# Task 4 -- Add license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that returns a structured license compliance report for the specified SBOM. The endpoint loads the license policy configuration, invokes the LicenseReportService to generate the report, and returns the LicenseReport as a JSON response.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- Handler function for the license report endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Register the new `/api/v2/sbom/{id}/license-report` route alongside existing SBOM routes
- `server/src/main.rs` -- Ensure the license policy configuration is loaded at startup and made available to the endpoint handler via Axum state/extension (if not already handled by existing config infrastructure)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: returns a `LicenseReport` JSON response containing packages grouped by license type with compliance flags. Response shape: `{ sbom_id: "...", policy_name: "...", groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/` -- see `get.rs` (GET /api/v2/sbom/{id}) for the established handler pattern: async function extracting path parameters, calling the service, and returning `Result<Json<T>, AppError>`.
- Route registration follows the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` -- add the new route alongside existing routes using the same Axum router builder approach.
- The handler should:
  1. Extract the SBOM ID from the path parameter
  2. Load the `LicensePolicy` from the configuration (via Axum state/extension)
  3. Call `LicenseReportService::generate_report()` with the SBOM ID and policy
  4. Return the `LicenseReport` as `Json<LicenseReport>`
- Error cases: return 404 if the SBOM does not exist, 500 for internal errors. Use `AppError` from `common/src/error.rs` with `.context()` wrapping.
- The endpoint should use the existing authentication middleware already applied to the `/api/v2/sbom` route group -- no additional auth configuration needed.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- GET /api/v2/sbom/{id} handler; follow the same async handler function signature, path parameter extraction, and error handling pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Route registration; follow the same router builder pattern to add the new route
- `common/src/error.rs` -- `AppError` enum; use for endpoint error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns a 200 response with the license report JSON
- [ ] Response matches the specified shape: `{ groups: [{ license: "...", packages: [...], compliant: true/false }] }`
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Endpoint is registered under the existing SBOM route group with proper authentication

## Test Requirements
- [ ] Integration test: successful license report generation returns 200 with correct JSON shape
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: response includes compliance flags matching the configured policy

## Verification Commands
- `cargo test -p fundamental` -- all tests pass including new endpoint tests
- `cargo build` -- project compiles with the new endpoint registered

## Dependencies
- Depends on: Task 1 -- Add license policy configuration model and loader (provides LicensePolicy for loading at startup)
- Depends on: Task 2 -- Add license compliance report model (provides LicenseReport response type)
- Depends on: Task 3 -- Add license report service (provides LicenseReportService for report generation)
