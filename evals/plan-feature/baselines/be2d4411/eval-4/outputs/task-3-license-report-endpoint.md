## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that returns a license compliance report for the specified SBOM. Wire up route registration in the sbom endpoints module and ensure the endpoint is mounted in the server.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new license-report route in the sbom router

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for GET /api/v2/sbom/{id}/license-report

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a `LicenseReport` JSON response with packages grouped by license type and compliance flags. Path parameter `id` is the SBOM identifier. Response shape: `{ groups: [{ license, spdx_id, packages, compliant }], summary: { total_packages, compliant_count, non_compliant_count } }`

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` — the existing GET handler for `/api/v2/sbom/{id}` demonstrates the conventional approach for path-parameter extraction, service invocation, and JSON response serialization.
- Route registration: add the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for existing routes (e.g., `.route("/:id", get(get::handler))` becomes `.route("/:id/license-report", get(license_report::handler))`). The server setup in `server/src/main.rs` already mounts the sbom module's routes, so no changes to `main.rs` are needed.
- The handler should:
  1. Extract the SBOM `id` from the path using Axum's `Path` extractor
  2. Call `LicenseReportService::generate_report(id)` from Task 2
  3. Return `Json(report)` on success or propagate `AppError` on failure
- Error handling: use `Result<Json<LicenseReport>, AppError>` as the handler return type, matching the pattern in `modules/fundamental/src/sbom/endpoints/get.rs`. The `AppError` enum in `common/src/error.rs` already implements `IntoResponse`.
- Per docs/constraints.md section 5: error handling must use `Result<T, AppError>` with `.context()` wrapping.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference handler implementation for path parameter extraction and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for the sbom module
- `common/src/error.rs::AppError` — error type that implements IntoResponse for Axum

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid LicenseReport JSON body
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Route is registered in the sbom endpoints module
- [ ] Response content-type is application/json
- [ ] Endpoint follows the same authentication/authorization pattern as existing sbom endpoints

## Test Requirements
- [ ] Handler unit test: valid SBOM ID returns 200 with correct JSON structure
- [ ] Handler unit test: non-existent SBOM ID returns 404
- [ ] Route registration test: verify the route is reachable at /api/v2/sbom/{id}/license-report

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo check -p trustify-server` — server compiles with new route

## Dependencies
- Depends on: Task 2 — Add license compliance report service (LicenseReportService::generate_report)

[sdlc-workflow] Description digest: sha256-md:f83218a0a66005f676612d0e658db804bf63c787772212f1a4a3cc3877106518
