## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that returns a license compliance report for the specified SBOM. The handler extracts the SBOM ID from the path, invokes the license compliance service, and returns the `LicenseReport` as a JSON response.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for the license report endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/api/v2/sbom/{id}/license-report` route

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a JSON `LicenseReport` containing packages grouped by license with compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true, policy_category: "approved" }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` which handles `GET /api/v2/sbom/{id}`. The license report handler should follow the same structure: extract path parameters, call the service, return the result as JSON.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing list and get routes. The route should be nested under the SBOM resource: `.route("/api/v2/sbom/:id/license-report", get(license_report))`.
- The handler should accept the SBOM ID as a path parameter (`axum::extract::Path<Uuid>` or similar), inject the database connection and license policy via Axum state/extensions, and delegate to `LicenseReportService::generate_report`.
- Per CONVENTIONS.md §Error handling: the handler must return `Result<Json<LicenseReport>, AppError>` with `.context()` wrapping on service call failures. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's .rs scope.
- Per CONVENTIONS.md §Endpoint registration: register the route in `endpoints/mod.rs` following the established pattern where each module's `endpoints/mod.rs` registers routes. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's .rs scope.
- Per CONVENTIONS.md §Caching: consider adding `tower-http` cache headers for the license report since policy evaluations for the same SBOM are deterministic until the policy or SBOM changes. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's .rs scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Pattern reference for SBOM endpoint handler structure (path extraction, service call, JSON response)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow
- `common/src/error.rs::AppError` — Error type implementing `IntoResponse` for automatic error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a valid `LicenseReport` JSON body
- [ ] Returns HTTP 404 with an appropriate error when the SBOM ID does not exist
- [ ] Route is registered in the SBOM module's endpoint configuration
- [ ] Response Content-Type is `application/json`

## Test Requirements
- [ ] Handler returns 200 with correct JSON structure for a valid SBOM with packages
- [ ] Handler returns 404 for a non-existent SBOM ID
- [ ] Handler returns 200 with empty groups for an SBOM with no packages

## Dependencies
- Depends on: Task 3 — License compliance service

## additional_fields
```json
{ "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```
