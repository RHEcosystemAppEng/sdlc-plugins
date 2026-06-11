# Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint that exposes the license compliance report for a given SBOM. This endpoint integrates the license report service (Task 3) with the Axum HTTP layer, following the existing endpoint conventions for route registration, error handling, and response serialization.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new license-report route alongside existing SBOM routes
- `server/src/main.rs` — Ensure the SBOM module routes (which now include license-report) are mounted (likely already handled by existing module registration, but verify)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report grouped by license type with compliance flags. Response shape: `{ sbom_id: String, groups: [{ license: String, packages: [{ name: String, version: String, transitive: bool }], compliant: bool, policy_status: String }], total_packages: number, compliant_count: number, non_compliant_count: number }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs`:
  - Extract the SBOM ID from the URL path using Axum's `Path` extractor
  - Accept a database connection from the application state
  - Call the `LicenseReportService` to generate the report
  - Return `Result<Json<LicenseReport>, AppError>` following the standard error handling pattern
- Route registration in `endpoints/mod.rs`: add `.route("/api/v2/sbom/:id/license-report", get(license_report::handler))` following the pattern used for existing SBOM routes (see `list.rs` and `get.rs` registrations).
- The handler should return HTTP 404 with an appropriate `AppError` if the SBOM ID does not exist.
- The handler should return HTTP 200 with the serialized `LicenseReport` on success.
- Per `docs/constraints.md` section 5.3: follow patterns referenced in implementation notes. Match the handler signature and error handling of `get.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Follow the same handler pattern (Path extractor, state injection, Result<Json<T>, AppError> return type)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Reference for route registration pattern
- `common/src/error.rs::AppError` — Use for error responses (404 not found, 500 internal error)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a valid `LicenseReport` JSON response for an existing SBOM
- [ ] Returns HTTP 404 when the SBOM ID does not exist
- [ ] Response JSON matches the specified shape with `groups`, `total_packages`, `compliant_count`, and `non_compliant_count` fields
- [ ] The endpoint is registered and accessible via the Axum router

## Test Requirements
- [ ] Integration test: call `GET /api/v2/sbom/{id}/license-report` for an SBOM with known package-license data and verify the response structure and compliance flags
- [ ] Integration test: call the endpoint with a non-existent SBOM ID and verify HTTP 404 response
- [ ] Integration test: verify response includes transitive dependencies when present

## Verification Commands
- `cargo build` — full project compiles without errors
- `cargo test -p trustify-fundamental` — module tests pass
- `cargo test --test api` — integration tests pass

## Documentation Updates
- `README.md` — Add the license report endpoint to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 2 — Add license compliance report model
- Depends on: Task 3 — Add license report service with transitive dependency walking
