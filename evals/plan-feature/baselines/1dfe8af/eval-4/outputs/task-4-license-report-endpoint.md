## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint handler for `GET /api/v2/sbom/{id}/license-report` that returns a license compliance report. This wires the service method from Task 3 into an Axum route handler, registers it with the SBOM module's router, and mounts it in the server.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler function for the license report endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `pub mod license_report;` and register the new route under `/api/v2/sbom/{id}/license-report`
- `server/src/main.rs` — Ensure the license policy is loaded at startup and made available via Axum state or extension

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a `LicenseReport` JSON response with packages grouped by license and compliance flags

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction and error handling.
- The handler should:
  1. Extract the SBOM `id` from the URL path using Axum's `Path` extractor.
  2. Retrieve the `LicensePolicy` from Axum's application state (loaded at server startup in `server/src/main.rs`).
  3. Call `SbomService::generate_license_report(id, policy, db)`.
  4. Return `Json(report)` on success or propagate `AppError` on failure.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes like `get.rs` and `list.rs`.
- In `server/src/main.rs`, load `LicensePolicy` from the config file path (e.g., `./license-policy.json`) and insert it into the Axum router state so handlers can access it.
- All handlers return `Result<T, AppError>` following the project convention from `common/src/error.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing SBOM GET handler; follow the same path extraction, service call, and response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow
- `common/src/error.rs::AppError` — Standard error type implementing `IntoResponse`

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON `LicenseReport`
- [ ] Response body contains `groups` array with `license`, `packages`, and `compliant` fields
- [ ] Non-existent SBOM ID returns HTTP 404
- [ ] License policy is loaded once at server startup, not per-request
- [ ] Route is registered alongside existing SBOM endpoints

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{valid-id}/license-report` returns 200 with expected JSON structure
- [ ] Integration test: `GET /api/v2/sbom/{invalid-id}/license-report` returns 404

## Dependencies
- Depends on: Task 3 — Implement license report service method

[sdlc-workflow] Description digest: sha256-md:ccdc5f430f099f81e604de018ea6f6e07801b202a36389c7fa8710cf21f6c73f
