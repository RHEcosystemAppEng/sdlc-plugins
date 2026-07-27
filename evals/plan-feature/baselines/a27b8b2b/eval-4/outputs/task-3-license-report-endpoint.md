## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that returns a structured license compliance report for a given SBOM. The endpoint invokes the `LicenseReportService` from Task 2 and returns the `LicenseReport` as a JSON response with the shape `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`.

The endpoint follows the existing Axum handler pattern and integrates with the SBOM module's route registration.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler function for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/license-report` route alongside existing SBOM routes
- `modules/fundamental/src/sbom/license_report/mod.rs` — Re-export service types needed by the endpoint if not already public

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a `LicenseReport` JSON response with grouped license data and compliance flags. Response shape: `{ groups: [{ license: string, packages: [{ name: string, version: string, purl: string }], compliant: bool }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler function structure, path parameter extraction, and error handling.
- The handler should:
  1. Extract the SBOM ID from the path parameter using Axum's `Path` extractor
  2. Load the license policy (from the configured JSON file or an injected policy service)
  3. Call `LicenseReportService::generate_report(sbom_id, db, policy)`
  4. Return `Json(report)` on success or map errors to `AppError` (from `common/src/error.rs`)
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same `Router::new().route(...)` pattern used for the existing `/api/v2/sbom` and `/api/v2/sbom/{id}` routes.
- The endpoint does NOT use `PaginatedResults<T>` since the report is a single structured response, not a list.
- All handlers return `Result<T, AppError>` per the codebase error handling convention.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing `GET /api/v2/sbom/{id}` handler. Follow the same pattern for path parameter extraction, database connection injection, and error mapping.
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration module. Add the new route alongside existing routes.
- `common/src/error.rs::AppError` — Error type implementing `IntoResponse`. Use for all error returns from the handler.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON `LicenseReport` for a valid SBOM ID
- [ ] Response JSON matches the contract: `{ groups: [{ license: string, packages: [...], compliant: bool }] }`
- [ ] Returns 404 for a non-existent SBOM ID
- [ ] Route is registered in the SBOM module's endpoint registration
- [ ] Endpoint is accessible via the Axum server (route mounted in `server/src/main.rs` via existing SBOM module mount)

## Test Requirements
- [ ] Integration test: call `GET /api/v2/sbom/{id}/license-report` with a valid SBOM — verify 200 status and correct response shape
- [ ] Integration test: call `GET /api/v2/sbom/{id}/license-report` with a non-existent SBOM ID — verify 404 status
- [ ] Integration test: verify response includes compliance flags matching the configured policy

## Verification Commands
- `cargo build --package trustify-fundamental` — verify compilation
- `cargo test --package trustify-fundamental -- license_report` — run license report tests

## Dependencies
- Depends on: Task 2 — Add license report service with transitive dependency resolution
