## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that returns a license compliance report for a given SBOM. This endpoint calls the license report service (Task 2) and returns the structured report as JSON. The endpoint follows the existing Axum handler pattern and integrates into the SBOM module's route registration.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report` that extracts the SBOM ID path parameter, calls the license report service, and returns the report as JSON

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/license-report` route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a license compliance report grouped by license type with compliance flags. Response shape: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` — extract path parameters using Axum extractors, call the service layer, and return `Result<Json<T>, AppError>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing SBOM routes (`list.rs`, `get.rs`). The existing pattern shows route registration using Axum's Router with method routing.
- The handler should:
  1. Extract the SBOM `id` from the path parameter
  2. Call `LicenseReportService::generate_report(id, db)` from Task 2
  3. Return the `LicenseReport` as `Json<LicenseReport>`
  4. Return `AppError` (404) if the SBOM ID does not exist
- Error handling: return `AppError` with appropriate status codes — 404 for SBOM not found, 500 for internal errors. Follow the pattern in `common/src/error.rs`.
- The endpoint does not need pagination since it returns a single report per SBOM. Do not use `PaginatedResults<T>` from `common/src/model/paginated.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the established GET endpoint pattern with path parameter extraction and service call
- `modules/fundamental/src/sbom/endpoints/mod.rs` — shows how routes are registered; add the new route following this pattern
- `common/src/error.rs::AppError` — the standard error type used by all handlers

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns a JSON response with the license report
- [ ] Response body matches the schema: `{ "groups": [{ "license": "...", "packages": [...], "compliant": true/false }] }`
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Returns 500 with proper error wrapping for internal errors
- [ ] The route is registered in the SBOM module's route configuration

## Test Requirements
- [ ] Integration test verifying `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid report for an existing SBOM
- [ ] Integration test verifying the response body contains correct license groups and compliance flags
- [ ] Integration test verifying 404 is returned for a non-existent SBOM ID
- [ ] Integration test verifying transitive dependency licenses are included in the report

## Verification Commands
- `cargo build -p trustify-fundamental` — should compile without errors
- `cargo test -p trustify-fundamental license_report` — should pass all unit tests
- `cargo test --test api license_report` — should pass integration tests

## Dependencies
- Depends on: Task 2 — Add license compliance report service logic
