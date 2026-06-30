# Task 3 -- Add license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` REST endpoint that generates and returns a license compliance report for the specified SBOM. This endpoint wires the license report service (Task 2) into the Axum HTTP layer and registers the route alongside existing SBOM endpoints. This is the primary user-facing API for the license compliance report feature (TC-9004).

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- Handler function for `GET /api/v2/sbom/{id}/license-report`; extracts SBOM ID from path, loads the license policy, calls LicenseReportService, and returns the report as JSON

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Add `pub mod license_report;` and register the new route in the existing SBOM route builder alongside `list.rs` and `get.rs`
- `server/src/main.rs` -- Ensure the license policy configuration is loaded at startup and made available to the handler (e.g., via Axum state/extension)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: Returns a license compliance report for the given SBOM. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/` -- see `get.rs` (GET /api/v2/sbom/{id}) for how to extract path parameters, call a service, and return a JSON response.
- See `modules/fundamental/src/sbom/endpoints/mod.rs` for how routes are registered -- add the license-report route using the same pattern as the existing `get` and `list` routes.
- The handler should return `Result<Json<LicenseReport>, AppError>` following the pattern in `get.rs`.
- Load the `LicensePolicy` from application state (injected via Axum's `State` or `Extension` extractor), not by reading the file on every request.
- In `server/src/main.rs`, load the license policy configuration file at startup and add it to the Axum application state so handlers can access it.
- Per CONVENTIONS.md (repository conventions): follow the `model/ + service/ + endpoints/` module pattern for endpoint registration.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust module scope.
- Ensure the endpoint returns appropriate HTTP status codes: 200 for success, 404 if the SBOM ID does not exist, 500 for internal errors.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- Reference implementation for a GET endpoint on a single SBOM by ID; follow the same pattern for path extraction, service call, and response.
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Route registration pattern; add the new route here following the existing structure.
- `common/src/error.rs::AppError` -- Error type that implements `IntoResponse` for Axum; use for all error returns.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns a 200 response with a JSON body containing license groups
- [ ] Each group contains a `license` string, a `packages` array, and a `compliant` boolean
- [ ] The endpoint returns 404 when the SBOM ID does not exist
- [ ] The license policy is loaded once at startup, not on every request
- [ ] The route is registered in the SBOM endpoint module and mounted by the server

## Test Requirements
- [ ] Integration test: call the endpoint with a valid SBOM ID and verify 200 response with correct JSON structure
- [ ] Integration test: call the endpoint with a non-existent SBOM ID and verify 404 response
- [ ] Integration test: verify that packages with non-compliant licenses are flagged in the response

## Verification Commands
- `cargo build` -- Verify the project compiles with the new endpoint
- `cargo test` -- Verify all tests pass including the new endpoint tests

## Dependencies
- Depends on: Task 2 -- Add license report model and service

<!-- [sdlc-workflow] Description digest: sha256-md:cd07eea828517e6abc06fb0035141da527cb6eaf56a9232c1f8136a9273c5635 -->
