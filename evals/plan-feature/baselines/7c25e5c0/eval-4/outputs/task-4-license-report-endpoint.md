## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint handler. This endpoint loads the license policy, calls the `LicenseReportService` to generate the compliance report, and returns the `LicenseReport` as a JSON response.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Endpoint handler for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the license-report route in the SBOM endpoint module

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a `LicenseReport` JSON response with packages grouped by license and compliance flags

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (GET handler for SBOM details) for route handler structure, path parameter extraction, and error response handling.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing SBOM routes, following the registration pattern used for `list.rs` and `get.rs`.
- The handler should:
  1. Extract the SBOM ID from the path parameter
  2. Load the `LicensePolicy` from the configured path
  3. Call `LicenseReportService::generate_report(sbom_id, policy)`
  4. Return `Json(report)` on success or `AppError` on failure
- Return 404 with appropriate error message when the SBOM ID does not exist (delegate to service error handling).
- Reference `server/src/main.rs` for how module routes are mounted on the Axum router.
- Per CONVENTIONS.md §Endpoint registration: register the route in the module's `endpoints/mod.rs`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Error handling: handler returns `Result<Json<LicenseReport>, AppError>`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint scope.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns a JSON response with the expected `{ groups: [...] }` structure
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Each group in the response includes `license`, `packages`, and `compliant` fields
- [ ] The endpoint is registered in the SBOM route module

## Test Requirements
- [ ] Integration test: call the endpoint with a valid SBOM ID and verify the response structure
- [ ] Integration test: call the endpoint with a non-existent SBOM ID and verify 404 response
- [ ] Integration test: verify response includes compliance flags based on the active policy

## Dependencies
- Depends on: Task 3 — License report service
