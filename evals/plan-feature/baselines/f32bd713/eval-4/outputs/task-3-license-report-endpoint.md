## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint for generating license compliance reports (TC-9004). The endpoint accepts an SBOM ID as a path parameter, invokes the license report service to generate the compliance report, and returns the structured ComplianceReport as JSON. Register the new route in the sbom module's endpoint configuration.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — GET handler function for the license report endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/license-report` route in the sbom endpoint router

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a ComplianceReport JSON object containing license groups with package lists and compliance flags. Response format: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}). The handler should:

1. Extract the SBOM ID from the path parameter
2. Load the license policy configuration
3. Call the LicenseReportService to generate the report
4. Return the ComplianceReport as a JSON response

Per CONVENTIONS.md §Error handling: the handler must return `Result<Json<ComplianceReport>, AppError>` with `.context()` wrapping on all fallible operations. See `common/src/error.rs` for the AppError enum and its IntoResponse implementation.
Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` endpoint handler scope.

Per CONVENTIONS.md §Endpoint registration: register the route in `modules/fundamental/src/sbom/endpoints/mod.rs`. The server/main.rs file already mounts the sbom module, so no changes are needed there.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint registration scope.

Per CONVENTIONS.md §Caching: consider configuring tower-http caching middleware in the route builder if compliance reports are cacheable. If reports should always reflect current data, skip caching.
Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` endpoint route builder scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET /api/v2/sbom/{id} handler pattern; follow its path parameter extraction and response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for adding new routes to the sbom module
- `common/src/error.rs::AppError` — standard error response handling with IntoResponse

## Acceptance Criteria
- [ ] GET /api/v2/sbom/{id}/license-report returns HTTP 200 with a valid ComplianceReport JSON body
- [ ] Response body matches the format: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- [ ] Returns HTTP 404 when the SBOM ID does not exist
- [ ] Route is registered and accessible at /api/v2/sbom/{id}/license-report
- [ ] Error responses follow the AppError pattern with appropriate HTTP status codes

## Test Requirements
- [ ] Verify endpoint returns HTTP 200 with correct ComplianceReport response format
- [ ] Verify endpoint returns HTTP 404 for a non-existent SBOM ID

## Dependencies
- Depends on: Task 2 — Add license compliance report service with transitive dependency resolution
