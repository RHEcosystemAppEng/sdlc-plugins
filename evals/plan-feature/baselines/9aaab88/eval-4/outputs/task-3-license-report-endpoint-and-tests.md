## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint `GET /api/v2/sbom/{id}/license-report` that invokes the license report service and returns the compliance report as JSON. Register the route in the SBOM endpoint module and mount it in the server. Add integration tests covering the full request-response cycle including compliant SBOMs, non-compliant SBOMs, and error cases.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report` that extracts the SBOM ID from the path, calls `LicenseReportService::generate_report()`, and returns the `LicenseReport` as JSON
- `tests/api/license_report.rs` — Integration tests for the license report endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `license-report` route under the existing `/api/v2/sbom/{id}` path, add `pub mod license_report;`
- `server/src/main.rs` — Verify SBOM module routes are already mounted (no change expected if SBOM endpoints are already registered, but confirm the new sub-route is reachable)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM, with packages grouped by license type and compliance flags based on the configured policy

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Follow the same handler pattern for path extraction, service invocation, and error response mapping
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Follow the existing route registration pattern to add the new sub-route
- `common/src/error.rs::AppError` — Reuse the existing error-to-response conversion for 404 (SBOM not found) and 500 (internal errors)
- `tests/api/sbom.rs` — Follow the same integration test patterns for test setup, database seeding, and assertion style

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs`: extract path parameters with `axum::extract::Path`, inject the service via Axum state, call the service method, and return `Json(report)`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing SBOM routes using `.route("/api/v2/sbom/:id/license-report", get(license_report::handler))` or the equivalent router method used by existing endpoints.
- The handler should return `Result<Json<LicenseReport>, AppError>` to leverage automatic error-to-HTTP-status conversion.
- For integration tests, follow the pattern in `tests/api/sbom.rs`: set up a test database, ingest a test SBOM with known packages and licenses, call the endpoint, and assert on the response structure and compliance flags.
- Per CONVENTIONS.md §Error handling: handler returns `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Endpoint registration: register the route in `endpoints/mod.rs` and ensure it is mounted via `server/main.rs`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint scope.
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/license_report.rs` matching the convention's `.rs` test file scope.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON body containing `{ groups: [...] }` for a valid SBOM
- [ ] Each group in the response contains `license`, `packages`, and `compliant` fields
- [ ] Request for a non-existent SBOM ID returns 404
- [ ] Response includes transitive dependency packages
- [ ] Non-compliant licenses are correctly flagged based on the policy configuration

## Test Requirements
- [ ] Integration test: ingest SBOM with mixed compliant/non-compliant licenses, verify response groups and compliance flags
- [ ] Integration test: request license report for non-existent SBOM ID, verify 404 response
- [ ] Integration test: ingest SBOM with only allowed licenses, verify all groups are marked compliant
- [ ] Integration test: ingest empty SBOM (no packages), verify response is 200 with empty groups array

## Dependencies
- Depends on: Task 2 — Implement license report service logic

[sdlc-workflow] Description digest: sha256-md:b9757f240fe3c9fc633c2a3a05c8e6dd3a3d3794ff945e9f893f6f849ce00dba
