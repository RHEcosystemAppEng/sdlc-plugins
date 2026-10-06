## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that returns a structured license compliance report for the specified SBOM. The endpoint delegates to the LicenseReportService (Task 3) and returns the report as a JSON response. Register the new route in the sbom endpoints module and ensure it is mounted by the server.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- defines the Axum handler function for the license report endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the `/api/v2/sbom/{id}/license-report` route
- `server/src/main.rs` -- verify sbom module routes are mounted (likely already mounted; confirm and update if needed)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: returns a `LicenseReportResponse` JSON body with packages grouped by license and compliance flags

## Implementation Notes
- Follow the endpoint handler patterns in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) for parameter extraction, service invocation, and response formatting.
- The handler should:
  1. Extract the SBOM ID from the path parameter
  2. Load the license policy configuration
  3. Call `LicenseReportService::generate_report()`
  4. Return the `LicenseReportResponse` as JSON with `StatusCode::OK`
  5. Return appropriate error responses (404 for unknown SBOM, 500 for internal errors)
- Per CONVENTIONS.md Endpoint registration: register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern; `server/src/main.rs` mounts all modules.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md Error handling: the handler returns `Result<T, AppError>` with `.context()` wrapping for all fallible operations.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` handler scope.
- Per CONVENTIONS.md Caching: consider adding `tower-http` cache configuration to the route builder for the license report endpoint, following the caching middleware pattern used by other endpoints.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's endpoint route builder scope.
- Per CONVENTIONS.md Module pattern: the endpoint file follows the `model/ + service/ + endpoints/` structure.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's module directory structure scope.

### Constraints (from docs/constraints.md)
- SS5.1: Keep changes scoped to the files listed in Files to Modify and Files to Create.
- SS5.2: Inspect existing endpoint handlers before writing to follow established patterns.
- SS5.3: Follow the patterns referenced in Implementation Notes.
- SS2.1: Commit must reference Jira issue ID in footer.
- SS2.2: Use Conventional Commits format.
- SS3.3: `gh pr create` must specify `--base main`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- GET handler pattern for extracting SBOM ID from path and returning a JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- route registration pattern to follow for adding the new route
- `common/src/error.rs::AppError` -- error type implementing IntoResponse for error handling in the handler

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON `LicenseReportResponse`
- [ ] Response body matches the specified shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- [ ] Endpoint returns HTTP 404 when the SBOM ID does not exist
- [ ] Endpoint returns HTTP 500 with error details for internal failures
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Route is accessible when the server starts (mounted via `server/src/main.rs`)

## Test Requirements
- [ ] Integration test: call the endpoint with a valid SBOM ID and verify HTTP 200 with correct response shape
- [ ] Integration test: call the endpoint with a non-existent SBOM ID and verify HTTP 404
- [ ] Integration test: verify the response contains license groups with compliance flags

## Verification Commands
- `cargo run -p trustify-server` -- start the server and confirm the endpoint is reachable
- `curl http://localhost:8080/api/v2/sbom/{test-id}/license-report` -- manually verify endpoint response

## Dependencies
- Depends on: Task 3 -- Add license compliance report service
