# Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint `GET /api/v2/sbom/{id}/license-report` that invokes the `LicenseReportService` (Task 2) and returns a structured license compliance report as JSON. The endpoint follows the existing Axum handler patterns in the SBOM endpoints module and integrates with the server's route mounting.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/license-report` route in the SBOM endpoint router
- `server/src/main.rs` — verify the SBOM module routes are already mounted (likely no change needed, but confirm)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for the license report endpoint

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a `LicenseReport` JSON response with structure `{ groups: [{ license: String, packages: [...], compliant: bool }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler function signature, path parameter extraction, service invocation, and JSON response formatting.
- The handler should:
  1. Extract the SBOM `id` from the path parameter
  2. Obtain the `LicenseReportService` from the Axum state/extension
  3. Call the service to generate the report
  4. Return the `LicenseReport` as a JSON response
- Use `Result<Json<LicenseReport>, AppError>` as the return type, consistent with the error handling pattern in `common/src/error.rs` where `AppError` implements `IntoResponse`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern as `get.rs` and `list.rs` route registration.
- The endpoint must be authenticated (follow the same auth middleware applied to existing SBOM endpoints).
- Consider cache configuration using `tower-http` caching middleware consistent with the project's caching conventions described in the repo structure.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the SBOM detail endpoint handler pattern (path extraction, service call, JSON response)
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates route registration and paginated response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for the SBOM module
- `common/src/error.rs::AppError` — error type that implements `IntoResponse` for Axum handlers

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON `LicenseReport` body
- [ ] Response structure matches `{ groups: [{ license: String, packages: [...], compliant: bool }] }`
- [ ] Returns HTTP 404 when the SBOM ID does not exist
- [ ] Endpoint uses the same authentication middleware as other SBOM endpoints
- [ ] Route is properly registered and accessible through the server

## Test Requirements
- [ ] Integration test: call the endpoint with a valid SBOM ID and verify the response shape and status 200
- [ ] Integration test: call the endpoint with a non-existent SBOM ID and verify 404 response
- [ ] Integration test: verify the response contains license groups with correct compliance flags

## Verification Commands
- `cargo test -p trustify-tests -- license_report` — run license report endpoint integration tests
- `curl -s http://localhost:8080/api/v2/sbom/{id}/license-report | jq .` — manual verification of response shape

## Dependencies
- Depends on: Task 2 — Add license report service with transitive dependency resolution
