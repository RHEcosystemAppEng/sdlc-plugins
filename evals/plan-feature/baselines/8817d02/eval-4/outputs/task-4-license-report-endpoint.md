# Task 4 — Add license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that returns a structured license compliance report for the specified SBOM. The endpoint calls the `LicenseReportService` (from Task 3) and returns the `LicenseReport` response. This is the primary API entry point for compliance teams and CI/CD pipelines to retrieve license compliance data.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — handler function for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new license-report route alongside existing SBOM routes
- `server/src/main.rs` — ensure the SBOM module routes (including the new endpoint) are mounted (may already be handled by existing route registration)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `LicenseReport` JSON response with packages grouped by license and compliance flags

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` (the `GET /api/v2/sbom/{id}` handler):
  - Extract the SBOM ID from the path parameter
  - Call the service layer to generate the report
  - Return the result as JSON with appropriate status codes
  - Return `Result<Json<LicenseReport>, AppError>` consistent with the project's error handling
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes (`list.rs`, `get.rs`). Follow the route registration pattern already used there.
- The endpoint path is `/api/v2/sbom/{id}/license-report` — this is a sub-resource of an existing SBOM, following the established URL pattern.
- If the SBOM ID does not exist, return a 404 error using the `AppError` enum from `common/src/error.rs`.
- Consider adding `tower-http` caching middleware configuration for this endpoint, as described in the Key Conventions section of the repository structure. License reports for the same SBOM are unlikely to change frequently.
- Per docs/constraints.md section 2 (Commit Rules): reference TC-9004 in commit footer; use Conventional Commits format.
- Per docs/constraints.md section 3 (PR Rules): branch named after Jira issue ID; post PR link to Jira task.
- Per docs/constraints.md section 5 (Code Change Rules): scope changes to listed files; inspect code before modifying; follow endpoint patterns from Implementation Notes.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET handler; follow the same Axum handler signature, path extraction, and error handling pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration; add the new route using the same `Router` builder pattern
- `common/src/error.rs::AppError` — reuse for 404 (SBOM not found) and 500 (report generation failure) error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid `LicenseReport` JSON body for an existing SBOM
- [ ] Response body matches the structure: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Route is registered and accessible through the Axum server

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` returns 200 and valid JSON for an SBOM with known packages and licenses
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` returns 404 for a non-existent SBOM ID
- [ ] Integration test: response contains correct license groupings and compliance flags matching the configured policy
- [ ] Integration test: endpoint handles an SBOM with zero packages gracefully (returns empty groups array)

## Verification Commands
- `cargo test --test api` — run integration tests against the test database
- `curl http://localhost:8080/api/v2/sbom/{id}/license-report` — manual verification against a running instance

## Documentation Updates
- `README.md` — add the license report endpoint to the API documentation section if one exists

## Dependencies
- Depends on: Task 1 — Add license compliance report model types
- Depends on: Task 3 — Add license compliance report service

sha256-md:4fe074a14783c92b5d782bb8322ee717c46cc5ffc589608ad8575b750f69f5b7
