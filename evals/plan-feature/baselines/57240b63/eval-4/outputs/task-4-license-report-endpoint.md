## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that returns a license compliance report for a given SBOM. Register the route in the SBOM endpoint module and ensure it is mounted by the server. This is the user-facing entry point for the license compliance report feature.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- Axum handler function for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the license-report route under the /api/v2/sbom/{id} path group
- `server/src/main.rs` -- verify the SBOM module routes (which now include license-report) are mounted (may already be handled by existing mount logic)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: returns a LicenseReport JSON response with packages grouped by license and compliance flags. Response shape: `{ "groups": [{ "license": "MIT", "packages": [{ "name": "...", "version": "...", "purl": "..." }], "compliant": true }], "compliant": true }`

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler function signature, path parameter extraction (`Path<Id>`), and error response handling.
- The handler should:
  1. Extract the SBOM ID from the path parameter using Axum's `Path` extractor.
  2. Load the `LicensePolicy` from the configured policy file path.
  3. Call `LicenseReportService::generate_report(db, sbom_id, &policy)` to produce the report.
  4. Return the `LicenseReport` as `Json<LicenseReport>` with `StatusCode::OK`.
  5. Return `AppError::NotFound` if the SBOM ID does not exist (propagated from the service layer).
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing SBOM routes (`list.rs`, `get.rs`), using the same router builder pattern.
- This endpoint returns a single report object, not a paginated list -- do not use `PaginatedResults<T>`.
- The route path nests under the existing `/api/v2/sbom/{id}` prefix with the `/license-report` suffix.

- Per CONVENTIONS.md §Endpoint Registration: register the route in `endpoints/mod.rs` following the existing route builder pattern, and ensure `server/src/main.rs` mounts the module.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

- Per CONVENTIONS.md §Error Handling: return `Result<Json<LicenseReport>, AppError>` from the handler and use `.context()` wrapping for service call errors.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- reference for handler function signature, Path extractor usage, and Json response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- reference for route registration and router builder pattern
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- additional reference for route registration consistency across modules
- `common/src/error.rs::AppError` -- error type for handler error responses (NotFound, InternalServerError)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns a JSON LicenseReport with HTTP 200
- [ ] Response body matches the expected shape: `{ "groups": [...], "compliant": bool }`
- [ ] Returns HTTP 404 for a non-existent SBOM ID
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Route is accessible through the server's mounted routes

## Test Requirements
- [ ] Handler returns HTTP 200 with a valid LicenseReport for a valid SBOM ID
- [ ] Handler returns HTTP 404 for a non-existent SBOM ID
- [ ] Response JSON structure matches the LicenseReport schema

## Verification Commands
- `cargo check -p trustify-module-fundamental` -- expected: compiles without errors
- `cargo check -p trustify-server` -- expected: compiles without errors (verifies route mounting)

## Dependencies
- Depends on: Task 1 -- License report model types
- Depends on: Task 3 -- License compliance service

---

[sdlc-workflow] Description digest: sha256-md:211388c2b96ba16f0e51b749fd1d38bd86ac305890442feb7516d5c68d34c58e
