## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` REST endpoint that returns a license compliance report for a given SBOM. The endpoint calls the license report service, loads the license policy from the configured file path, and returns the grouped license data with compliance flags as a JSON response.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — add route registration for the license-report endpoint
- `server/src/main.rs` — no changes needed if sbom module routes are already mounted (verify during implementation)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — implement the GET handler for `/api/v2/sbom/{id}/license-report`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a `LicenseReport` JSON response containing packages grouped by license with compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [{ name: "pkg", version: "1.0" }], compliant: true }], total_packages: 42, compliant_count: 10, non_compliant_count: 2 }`

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — extract the SBOM ID from the path parameter, call the service, return JSON.
- Register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing `list` and `get` routes. The existing pattern uses Axum's `Router::new().route(...)` chaining.
- The handler function should:
  1. Extract the SBOM ID from the path using Axum's `Path` extractor
  2. Load the `LicensePolicy` from a configurable file path (environment variable or default path like `config/license-policy.json`)
  3. Call `LicenseReportService::generate_report(sbom_id, &policy)` 
  4. Return the `LicenseReport` as JSON with `StatusCode::OK`
  5. Return `AppError::NotFound` if the SBOM ID does not exist
- Use `common/src/error.rs::AppError` for error handling — the handler should return `Result<Json<LicenseReport>, AppError>` following the pattern in existing endpoint handlers.
- Per constraints doc section 2 (Commit Rules): use Conventional Commits format, reference TC-9004 in the footer, include `--trailer="Assisted-by: Claude Code"`.
- Per constraints doc section 3 (PR Rules): name the branch after the Jira issue ID, post the PR link as a comment on TC-9004.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the exact pattern: path parameter extraction, service call, JSON response, error handling with `AppError`
- `modules/fundamental/src/sbom/endpoints/mod.rs` — shows how routes are registered in the sbom module; the new route follows this pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — shows the list endpoint pattern for reference on how Axum handlers are structured in this module
- `common/src/error.rs::AppError` — error type that implements `IntoResponse` for Axum

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns a 200 JSON response with the `LicenseReport` structure
- [ ] Non-existent SBOM ID returns a 404 error
- [ ] License policy is loaded from a configurable path
- [ ] Response contains packages grouped by license with correct compliance flags
- [ ] Endpoint is registered in the sbom module route tree

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` with a valid SBOM returns 200 with correct grouped data
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` with non-existent SBOM returns 404
- [ ] Integration test: verify response structure matches `LicenseReport` schema (groups, total_packages, compliant_count, non_compliant_count)
- [ ] Integration test: verify non-compliant licenses are correctly flagged when a deny-list policy is configured

## Verification Commands
- `cargo test --test api license_report` — run the license report integration tests, expect all to pass
- `cargo build` — verify the project compiles with the new endpoint

## Documentation Updates
- `README.md` — add the new `GET /api/v2/sbom/{id}/license-report` endpoint to the API documentation section, including request parameters, response shape, and example usage

## Dependencies
- Depends on: Task 1 — Add license report model types
- Depends on: Task 2 — Implement license report service

[sdlc-workflow] Description digest: sha256:b1461c4bceae79c9e682b9de848f299e36cb10c4d945e60d60aec570b8e4a712
