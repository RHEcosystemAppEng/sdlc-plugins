## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that returns a license compliance report for a given SBOM. The endpoint delegates to the `LicenseReportService` and returns the grouped license data with compliance flags. This task also registers the new route in the SBOM endpoint module.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the license report route under `/api/v2/sbom/{id}/license-report`
- `server/src/main.rs` — verify SBOM module routes are mounted (likely already mounted; confirm and add if needed)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — GET handler for the license report endpoint

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a `LicenseReport` JSON response with structure `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the endpoint handler pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) — the handler extracts the SBOM ID from the path, calls the service, and returns the result as JSON.
- The handler function signature should follow the Axum extractor pattern: `async fn get_license_report(Path(id): Path<Uuid>, ...) -> Result<Json<LicenseReport>, AppError>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing registration pattern used for `list.rs` and `get.rs`.
- The `server/src/main.rs` already mounts the SBOM module's routes — verify this and confirm the new route is accessible without additional changes.
- Use `.context()` wrapping on all error paths per the error handling convention.
- Per CONVENTIONS.md Key Conventions: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md Key Conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust endpoint scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for GET handler pattern with path parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for list endpoint pattern
- `common/src/error.rs::AppError` — error type that implements `IntoResponse`

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON `LicenseReport` for a valid SBOM ID
- [ ] Response JSON matches the shape `{ groups: [{ license: "<spdx-id>", packages: [...], compliant: <bool> }] }`
- [ ] Endpoint returns HTTP 404 for a non-existent SBOM ID
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Route is accessible through the server's mounted SBOM module routes

## Test Requirements
- [ ] GET request to `/api/v2/sbom/{id}/license-report` returns 200 with valid JSON for an SBOM with packages
- [ ] GET request to `/api/v2/sbom/{non-existent-id}/license-report` returns 404
- [ ] Response body deserializes to `LicenseReport` with correct structure
- [ ] Response includes compliance flags based on the configured policy

## Verification Commands
- `cargo test --package fundamental -- license_report` — runs license report unit tests
- `cargo test --test api -- license_report` — runs license report integration tests

## Dependencies
- Depends on: Task 2 — Add license compliance report service
