# Task 4 -- Add license report endpoint

**Summary:** Add GET /api/v2/sbom/{id}/license-report endpoint

**Priority:** Major
**Fix Versions:** RHTPA 1.5.0
**Labels:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that returns a license compliance report for the specified SBOM. The endpoint uses the `LicenseReportService` (Task 3) to generate the report and returns it as a JSON response.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- handler for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the new `/license-report` route under the existing `/api/v2/sbom` prefix
- `server/src/main.rs` -- ensure the license policy is loaded at startup and made available via Axum state (if not already handled by the module's route registration)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: returns a `LicenseReport` JSON response containing packages grouped by license with compliance flags

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/` -- see `get.rs` (GET /api/v2/sbom/{id}) for the handler signature, path parameter extraction, Axum state access, and error handling pattern
- Handler function signature should follow the pattern: `async fn license_report(Path(id): Path<String>, State(service): State<...>) -> Result<Json<LicenseReport>, AppError>`
- Register the route in `endpoints/mod.rs` following the existing pattern -- see how `get.rs` and `list.rs` routes are registered
- Mount the license policy configuration in the application state at startup in `server/src/main.rs` -- load from the `license-policy.json` config file
- The endpoint returns the full `LicenseReport` struct (from Task 2), not `PaginatedResults<T>`, since this is a report aggregation endpoint, not a list endpoint
- Return appropriate HTTP status codes: 200 for success, 404 if the SBOM ID is not found, 500 for internal errors
- Per CONVENTIONS.md (Key Conventions -- Error handling): handler returns `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` module scope.
- Per CONVENTIONS.md (Key Conventions -- Endpoint registration): register routes in the module's `endpoints/mod.rs`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- reference for handler pattern, path parameter extraction, and error responses
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- reference for route registration pattern
- `common/src/error.rs::AppError` -- error type implementing `IntoResponse`
- `server/src/main.rs` -- reference for application state setup and module mounting

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid `LicenseReport` JSON body
- [ ] Response body matches the required shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Route is properly registered and accessible through the server

## Test Requirements
- [ ] Integration test: endpoint returns 200 with correct report structure for an SBOM with known license data
- [ ] Integration test: endpoint returns 404 for a non-existent SBOM ID
- [ ] Integration test: response includes transitive dependency packages
- [ ] Integration test: compliance flags in response match the configured license policy

## Verification Commands
- `cargo test --test api license_report` -- run license report integration tests (expected: all pass)
- `curl -s http://localhost:8080/api/v2/sbom/{test-id}/license-report | jq .` -- verify response shape manually

## Documentation Updates
- `README.md` -- add license report endpoint to the API overview section

## Dependencies
- Depends on: Task 2 -- Add license compliance report model structs
- Depends on: Task 3 -- Add license report service
