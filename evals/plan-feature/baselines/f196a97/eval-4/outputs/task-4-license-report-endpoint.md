# Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint handler for the license compliance report. This endpoint accepts an SBOM ID, loads the license policy, invokes the LicenseReportService, and returns the structured compliance report. The endpoint follows the existing Axum handler patterns and is registered under the SBOM route namespace.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new license-report route alongside existing SBOM routes
- `server/src/main.rs` — Ensure the SBOM module routes (which now include license-report) are mounted (likely already handled by existing SBOM route registration)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint patterns in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`:
  - Use Axum `Path` extractor for the SBOM ID
  - Return `Result<Json<LicenseReport>, AppError>` from the handler
  - Use `.context()` for error wrapping
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern — the new route should be nested under the SBOM routes (e.g., `.route("/:id/license-report", get(license_report::handler))`)
- Load the LicensePolicy at startup or on each request from the configuration file. Consider whether to load once via Axum state/extension or per-request — follow the existing patterns in `server/src/main.rs` for configuration injection
- The handler should:
  1. Extract SBOM ID from the path
  2. Get LicensePolicy from application state or load from config
  3. Call `LicenseReportService::generate_report()`
  4. Return the LicenseReport as JSON
- For non-existent SBOM IDs, return HTTP 404 using the existing `AppError` mapping

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Follow its handler pattern (Path extraction, service call, error handling)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Reference for route registration pattern
- `common/src/error.rs::AppError` — Existing error-to-HTTP-status mapping

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with the license compliance report JSON
- [ ] Response matches the specified shape: `{ groups: [{ license, packages, compliant }] }`
- [ ] Returns HTTP 404 for non-existent SBOM IDs
- [ ] Route is correctly registered under the SBOM namespace

## Test Requirements
- [ ] Integration test: call `GET /api/v2/sbom/{id}/license-report` for an SBOM with known license data, verify 200 response with correct body shape
- [ ] Integration test: call endpoint with a non-existent SBOM ID, verify 404 response
- [ ] Integration test: verify response content-type is `application/json`

## Verification Commands
- `cargo test --test api` — Run API integration tests and verify the new license-report tests pass
- `cargo build` — Verify the project compiles with the new endpoint registered

## Documentation Updates
- `README.md` — Add the license report endpoint to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 3 — Add license report service with compliance checking
