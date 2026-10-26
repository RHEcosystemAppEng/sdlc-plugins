# Task 3 — Add license report endpoint and register route

## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint handler for `GET /api/v2/sbom/{id}/license-report` that invokes the license compliance report service and returns the structured report as JSON. Register the route in the SBOM endpoint module and ensure it is mounted in the Axum server.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/license-report` route
- `server/src/main.rs` — ensure SBOM module routes include the new endpoint (may already be covered by existing mount)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — endpoint handler for `GET /api/v2/sbom/{id}/license-report`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `LicenseReport { groups: [{ license: "MIT", packages: [{ name: "...", version: "...", purl: "..." }], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `list.rs` for handler function signatures and response construction.
- The handler should:
  1. Extract the SBOM `{id}` path parameter
  2. Obtain a database connection from the Axum state
  3. Call `LicenseReportService::generate_report(sbom_id)` from Task 2
  4. Return the `LicenseReport` as a JSON response with status 200
  5. Return appropriate error responses (404 for non-existent SBOM, 500 for internal errors)
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing SBOM routes (GET list, GET by id).
- The `server/src/main.rs` already mounts SBOM module routes — verify this covers the new endpoint or add the mount if needed.
- Per CONVENTIONS.md §Endpoint Registration: register the route in the module's `endpoints/mod.rs` and verify it is mounted in `server/src/main.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Error Handling: the handler must return `Result<Json<LicenseReport>, AppError>` with `.context()` wrapping on service errors.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Module Pattern: place the endpoint in `endpoints/license_report.rs` within the SBOM module.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's endpoint directory scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET endpoint handler for SBOM details; demonstrates path parameter extraction and error handling
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing list endpoint demonstrating query parameter handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow for adding the new route
- `common/src/error.rs::AppError` — error type implementing IntoResponse for Axum error handling

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON `LicenseReport` body
- [ ] Response JSON matches the contract: `{ groups: [{ license: string, packages: [...], compliant: bool }] }`
- [ ] Returns HTTP 404 when the SBOM ID does not exist
- [ ] Returns HTTP 500 with appropriate error body on internal service errors
- [ ] Route is registered in the SBOM endpoint module and accessible through the server

## Test Requirements
- [ ] Endpoint returns 200 with valid license report for an existing SBOM
- [ ] Endpoint returns 404 for non-existent SBOM ID
- [ ] Response Content-Type is application/json
- [ ] Response body conforms to the `LicenseReport` schema

## Verification Commands
- `cargo build -p trustify-server` — server compiles with new route
- `cargo test -p trustify-fundamental -- license_report` — endpoint unit tests pass

## Dependencies
- Depends on: Task 1 — Add license report model types and policy configuration
- Depends on: Task 2 — Implement license compliance report service
