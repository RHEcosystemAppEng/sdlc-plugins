## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint handler that calls the license report service and returns the grouped license compliance report. The endpoint follows the existing Axum handler pattern and is registered under the SBOM module's route tree.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/license-report` route under the existing `/api/v2/sbom/{id}` path

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a license compliance report for the given SBOM, response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure, path parameter extraction, and error handling.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust module file scope.
- Per Key Conventions (Error handling): handler returns `Result<Json<LicenseReport>, AppError>` with `.context()` wrapping on service calls.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust source file scope.
- Per Key Conventions (Endpoint registration): add the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs`. The route should be nested under the existing `/api/v2/sbom/{id}` prefix.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust source file scope.
- Extract the SBOM ID from the path using Axum's `Path` extractor, matching the pattern in `get.rs`.
- Inject the license report service (or `SbomService`) via Axum's state/extension mechanism, following the existing dependency injection pattern.
- Return `Json<LicenseReport>` on success, `AppError` on failure (SBOM not found, policy file error, etc.).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for path parameter extraction and handler structure
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for response serialization pattern
- `common/src/error.rs::AppError` — error type implementing `IntoResponse`

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with `LicenseReport` JSON for a valid SBOM
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 404 for a non-existent SBOM ID
- [ ] Response content type is `application/json`
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Handler follows the existing Axum handler pattern (Result<Json<T>, AppError>)

## Test Requirements
- [ ] Verify endpoint returns 200 with correct JSON shape for an SBOM with known license data
- [ ] Verify endpoint returns 404 for a non-existent SBOM ID
- [ ] Verify response includes `groups` array with `license`, `packages`, and `compliant` fields
- [ ] Verify endpoint is accessible at the correct path `/api/v2/sbom/{id}/license-report`

## Verification Commands
- `cargo test --test api -- license_report` — run license report integration tests, expect all tests to pass
- `cargo clippy --all-targets` — verify no warnings in new endpoint code

## Dependencies
- Depends on: Task 3 — Implement license report service
