# Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that returns a structured license compliance report for a given SBOM. The endpoint calls the license report service method (Task 2) and returns the grouped license data with compliance flags as JSON.

This is the user-facing API surface for TC-9004, consumed by compliance officers and CI/CD pipelines.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the license-report route alongside existing SBOM routes (list, get)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `LicenseReport` JSON response with grouped license data and compliance flags. Response shape: `{ "groups": [{ "license": "MIT", "packages": [{ "name": "...", "version": "...", "purl": "..." }], "compliant": true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) for handler function signature, path parameter extraction, error handling, and response serialization.
- The handler should:
  1. Extract the SBOM ID from the path parameter
  2. Load the license policy configuration
  3. Call `SbomService::generate_license_report(sbom_id, db, policy)`
  4. Return the `LicenseReport` as a JSON response
- Use `axum::extract::Path` for path parameter extraction, consistent with `get.rs`.
- Return `Result<Json<LicenseReport>, AppError>` following the error handling convention.
- Register the route in `endpoints/mod.rs` following the pattern used for the existing `list.rs` and `get.rs` routes. The route should be `.route("/api/v2/sbom/:id/license-report", get(license_report))`.
- Return appropriate HTTP status codes: 200 for success, 404 if SBOM not found, 500 for internal errors.
- Consider adding `tower-http` caching middleware configuration for the route, as noted in the Key Conventions (caching configuration in endpoint route builders).
- Per CONVENTIONS.md: follow the endpoints module pattern where each endpoint is a separate file within `endpoints/`. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's endpoints directory scope.
- Per docs/constraints.md section 2: commits must follow Conventional Commits format and reference TC-9004.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — GET /api/v2/sbom/{id} handler; follow the same pattern for path extraction, service call, and response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern; add the new route alongside existing ones
- `common/src/error.rs::AppError` — error handling type used by all handlers via `IntoResponse` implementation
- `modules/fundamental/src/advisory/endpoints/get.rs` — another GET-by-ID pattern for reference

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON body matching the `LicenseReport` schema
- [ ] Response body contains `groups` array with `license`, `packages`, and `compliant` fields per group
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Endpoint is registered in the SBOM route group
- [ ] Response uses correct Content-Type (`application/json`)

## Test Requirements
- [ ] Integration test for successful license report generation (200 response with correct JSON structure)
- [ ] Integration test for non-existent SBOM ID (404 response)
- [ ] Integration test verifying non-compliant licenses are flagged in the response

## Verification Commands
- `cargo test --package trustify-server -- license_report` — run endpoint integration tests
- `curl -s http://localhost:8080/api/v2/sbom/{id}/license-report | jq .` — manual verification of endpoint response

## Documentation Updates
- `README.md` — add the new endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 2 — Add license compliance service for SBOM packages
