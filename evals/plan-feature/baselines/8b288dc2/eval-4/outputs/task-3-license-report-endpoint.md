## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that generates and returns a license compliance report for a given SBOM. The endpoint loads the license policy configuration, invokes the license report service, and returns the structured report response.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- add route registration for the new license-report endpoint
- `server/src/main.rs` -- verify the sbom module route mounting includes the new endpoint (may not need changes if routes are auto-registered)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- implement the GET handler for `/api/v2/sbom/{id}/license-report`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: returns a `LicenseReport` JSON response with packages grouped by license type and compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` -- handler function takes `Path<String>` for the SBOM ID, uses Axum extractors, and returns `Result<Json<T>, AppError>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes like `list.rs` and `get.rs`. Use the existing route registration pattern (likely `Router::new().route(...)` composition).
- Load the `LicensePolicy` from the JSON configuration file. Consider using a shared application state or config extractor (check how existing configuration is accessed in `server/src/main.rs`).
- Call `LicenseReportService::generate_report` and return the result as `Json<LicenseReport>`.
- Return `404 Not Found` when the SBOM ID does not exist.
- Return `200 OK` with the report when successful.
- Per CONVENTIONS.md (Key Conventions): endpoint registration follows the pattern in each module's `endpoints/mod.rs`; routes are mounted from `server/main.rs`.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- existing SBOM GET endpoint handler; follow the same Axum extractor and response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- route registration pattern for the sbom module
- `common/src/error.rs::AppError` -- error handling for 404 and other error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid `LicenseReport` JSON response
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Response contains packages grouped by license with compliance flags
- [ ] Response content type is `application/json`

## Test Requirements
- [ ] Integration test: successful license report generation returns 200 with expected structure
- [ ] Integration test: request for non-existent SBOM ID returns 404

## Documentation Updates
- `README.md` -- add the new license-report endpoint to the API documentation section if one exists

## Dependencies
- Depends on: Task 2 -- Add license report service

## Description Digest
sha256-md:b50106eb603450b9eb8f836c45ee92e0db8baec6610b24034ac513e6b698a9e1
