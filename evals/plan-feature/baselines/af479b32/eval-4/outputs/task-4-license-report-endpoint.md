# Task 4 — Add license report REST endpoint

**Summary:** Add GET /api/v2/sbom/{id}/license-report endpoint

**Epic:** TC-9004: License report service and API

## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that generates and returns a license compliance report for a given SBOM. The endpoint calls the `LicenseReportService` (Task 3) and returns the `LicenseReport` as a JSON response.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new license-report route alongside existing SBOM routes
- `server/src/main.rs` — ensure the sbom module routes (which now include license-report) are mounted (may require no changes if the sbom module is already fully mounted)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a `LicenseReport` JSON response with status 200, or appropriate error status (404 for unknown SBOM, 500 for internal errors)

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`). The handler should:
  1. Extract the `id` path parameter
  2. Call `LicenseReportService::generate_report(id)` 
  3. Return `Ok(Json(report))` on success
  4. Return the appropriate `AppError` variant on failure (the `IntoResponse` impl in `common/src/error.rs` handles error conversion)
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern. The route should be nested under the existing `/api/v2/sbom` prefix.
- Use `Result<Json<LicenseReport>, AppError>` as the handler return type, matching the pattern in existing endpoint handlers.
- The handler receives its dependencies (database connection, license policy) through Axum's state extraction, consistent with how `SbomService` is accessed in `get.rs` and `list.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the handler pattern for `GET /api/v2/sbom/{id}` including path parameter extraction, service invocation, and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — demonstrates route registration pattern for the sbom module
- `common/src/error.rs::AppError` — the error type with `IntoResponse` implementation; reuse for handler error returns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid `LicenseReport` JSON body
- [ ] Response body matches the shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Route is registered and accessible through the server
- [ ] Endpoint follows the same authentication/authorization requirements as existing SBOM endpoints

## Test Requirements
- [ ] Test successful report generation returns 200 with correct JSON shape
- [ ] Test that a request for a non-existent SBOM returns 404
- [ ] Test that the response includes packages grouped by license with compliance flags

## Dependencies
- Depends on: Task 1 — Add license report response model types
- Depends on: Task 3 — Add license report service with transitive dependency resolution
