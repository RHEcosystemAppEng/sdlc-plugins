## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that generates and returns a license compliance report for the specified SBOM. Register the route in the sbom endpoints module following the established endpoint registration pattern.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the new `/api/v2/sbom/{id}/license-report` route in the sbom router

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- implement the GET handler that calls `LicenseReportService::generate_report` and returns the `LicenseReport` as JSON

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: returns a `LicenseReport` JSON response with packages grouped by license type and compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [{ name, version, purl }], compliant: true }] }`

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for extracting the SBOM ID path parameter and returning JSON responses.
- The handler should:
  1. Extract the SBOM `{id}` from the path
  2. Instantiate or inject `LicenseReportService`
  3. Call `generate_report(id)` to produce the `LicenseReport`
  4. Return the report as JSON with `StatusCode::OK`
  5. Return `AppError::NotFound` if the SBOM ID does not exist
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing sbom routes (list, get). Follow the same route builder pattern used for `list.rs` and `get.rs`.
- Per CONVENTIONS.md §Endpoint Registration: register routes in endpoints/mod.rs; the server mounts all modules from `server/src/main.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` and use `.context()` wrapping for all error paths.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- reference implementation for GET endpoint with path parameter extraction and JSON response
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference for route handler registration pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- existing route registration to follow the same pattern
- `common/src/error.rs::AppError` -- error type for handler return values

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a valid `LicenseReport` JSON response
- [ ] The response shape matches `{ groups: [{ license, packages, compliant }] }`
- [ ] Returns HTTP 404 when the SBOM ID does not exist
- [ ] Route is registered in the sbom endpoints module alongside existing routes
- [ ] Error responses use `AppError` with appropriate status codes

## Test Requirements
- [ ] Endpoint returns 200 with correct JSON shape for a valid SBOM with package license data
- [ ] Endpoint returns 404 for a non-existent SBOM ID
- [ ] Response includes compliance flags based on the configured policy
- [ ] Response includes transitive dependency licenses

## Verification Commands
- `cargo build -p trustify-fundamental` -- compiles without errors
- `cargo test -p trustify-fundamental -- license_report` -- endpoint handler tests pass

## Dependencies
- Depends on: Task 2 -- Implement license compliance report service
