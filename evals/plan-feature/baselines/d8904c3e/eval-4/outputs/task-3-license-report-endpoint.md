## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` REST endpoint that generates and
returns a license compliance report for a given SBOM. The endpoint loads the
license policy configuration, invokes the `LicenseReportService` to produce the
report, and returns the structured JSON response.

This endpoint enables compliance officers to retrieve a one-click license audit
and CI/CD pipelines to implement automated compliance gates by checking the
`compliant` flag on each license group.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- Axum handler function for `GET /api/v2/sbom/{id}/license-report`; extracts SBOM ID from path, loads policy, calls service, returns JSON response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Register the `/api/v2/sbom/{id}/license-report` route in the SBOM module's route configuration

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: Returns a license compliance report for the specified SBOM. Response shape: `{ groups: [{ license: string, packages: [{ name: string, version: string, purl: string }], compliant: bool }] }`. Returns 404 if SBOM ID does not exist. Returns 200 with the report on success.

## Implementation Notes
- Follow the endpoint pattern established in
  `modules/fundamental/src/sbom/endpoints/get.rs` and
  `modules/fundamental/src/sbom/endpoints/list.rs` -- each endpoint file defines
  an async handler function that receives Axum extractors and returns
  `Result<Json<T>, AppError>`.
- Per CONVENTIONS.md Section "Error handling": the handler must return
  `Result<Json<LicenseReport>, AppError>` with `.context()` wrapping on all
  fallible operations.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs`
  matching the convention's `.rs` endpoint handler scope.
- Per CONVENTIONS.md Section "Endpoint registration": register the new route in
  `modules/fundamental/src/sbom/endpoints/mod.rs` using the same pattern as
  existing SBOM routes (e.g., `.route("/api/v2/sbom/:id/license-report", get(...))`).
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching
  the convention's endpoint registration scope.
- Per CONVENTIONS.md Section "Module pattern": place the endpoint handler in the
  `endpoints/` directory following the `model/ + service/ + endpoints/` structure.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs`
  matching the convention's module structure scope.
- The handler should:
  1. Extract the SBOM ID from the path parameter
  2. Load the license policy (from config file or injected state)
  3. Call `LicenseReportService::generate_report(sbom_id, policy)`
  4. Return `Json(report)` on success or propagate the error
- Consider adding the policy file path to the application configuration/state so
  it can be injected into the handler via Axum's `State` extractor.
- Do NOT add any other endpoints beyond `GET /api/v2/sbom/{id}/license-report`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- demonstrates the handler
  pattern for a single-resource SBOM endpoint with path parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- shows route registration
  pattern for SBOM endpoints
- `common/src/error.rs::AppError` -- the error type all handlers return;
  implements `IntoResponse` for automatic HTTP error conversion

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with the license report JSON
- [ ] Response matches the documented shape: `{ groups: [{ license, packages, compliant }] }`
- [ ] Returns HTTP 404 when the SBOM ID does not exist
- [ ] Route is registered in the SBOM module's endpoint configuration
- [ ] No other endpoints are added (no admin, debug, internal, or exec endpoints)

## Test Requirements
- [ ] Handler returns 200 with correct report structure for a valid SBOM with packages and licenses
- [ ] Handler returns 404 for a non-existent SBOM ID
- [ ] Response content type is `application/json`

## Verification Commands
- `cargo check -p trustify-module-fundamental` -- compiles without errors
- `cargo check -p trustify-server` -- server binary compiles with new route

## Dependencies
- Depends on: Task 1 -- Add license report model types and policy configuration
- Depends on: Task 2 -- Implement license compliance report service
