# Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint that exposes the license compliance report for a given SBOM. The endpoint calls the `LicenseReportService` and returns the structured report as JSON. Register the route in the SBOM endpoints module following the established endpoint registration pattern.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- Axum handler for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Register the `/license-report` route under the existing `/api/v2/sbom/{id}` path
- `server/src/main.rs` -- Verify the SBOM module routes are mounted (likely already done; modify only if the new route requires explicit registration)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: Returns a license compliance report for the specified SBOM. Response shape: `{ "groups": [{ "license": "MIT", "packages": [{ "name": "serde", "version": "1.0", "purl": "pkg:cargo/serde@1.0" }], "compliant": true }], "compliant": true }`

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}). The handler should:
  1. Extract the SBOM ID from the path parameter
  2. Call `LicenseReportService::generate_report(sbom_id)`
  3. Return the `LicenseReport` as a JSON response
  4. Return appropriate HTTP errors (404 for non-existent SBOM, 500 for internal errors)
- **Error handling**: use `Result<Json<LicenseReport>, AppError>` as the return type, consistent with all handlers in the repository.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's endpoints directory scope.
- **Route registration**: add the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs`. The route should be nested under the existing `/api/v2/sbom/{id}` prefix.
- The endpoint does NOT return `PaginatedResults<T>` since it returns a single aggregated report, not a list. This follows the same pattern as detail endpoints (`get.rs`).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- GET /api/v2/sbom/{id} handler; follow the same path parameter extraction, error handling, and response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Route registration pattern; add the new route here
- `common/src/error.rs::AppError` -- Error type for handler return values

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON license compliance report
- [ ] Response JSON matches the documented shape with `groups` array and top-level `compliant` field
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Returns appropriate error when the SBOM has no package data
- [ ] Route is registered and accessible at the correct path

## Test Requirements
- [ ] Handler returns 200 and valid JSON for an SBOM with license data
- [ ] Handler returns 404 for a non-existent SBOM ID
- [ ] Response content-type is `application/json`
- [ ] Response body deserializes to the expected `LicenseReport` structure

## Verification Commands
- `cargo build --package fundamental` -- Verify the module compiles with the new endpoint
- `curl -s http://localhost:8080/api/v2/sbom/{id}/license-report | jq .` -- Manual verification of the endpoint response

## Dependencies
- Depends on: Task 1 -- Add license report model types and policy configuration
- Depends on: Task 2 -- Add license report service with dependency tree traversal
