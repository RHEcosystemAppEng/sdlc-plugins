## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that returns a license compliance report for the specified SBOM. The endpoint calls the license report service and returns the grouped report as JSON. This completes the API surface for the license compliance feature.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the license-report route alongside existing SBOM routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- endpoint handler for GET /api/v2/sbom/{id}/license-report

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: returns a license compliance report grouped by license type with compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler signature and path parameter extraction
- Use `Result<Json<LicenseReport>, AppError>` as the return type
- Extract the SBOM `{id}` path parameter following the same pattern as the existing `get.rs` handler
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing list and get routes
- Load the license policy configuration from the JSON config file at application startup or per-request (follow existing config loading patterns in the codebase)
- Per CONVENTIONS.md Error handling: return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md Endpoint registration: register the route in `endpoints/mod.rs` following the existing route registration pattern. See `modules/fundamental/src/sbom/endpoints/mod.rs` for the established pattern.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- existing SBOM GET handler to follow for path parameter extraction and response patterns
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- existing route registration showing how to add new routes to the SBOM router
- `common/src/error.rs::AppError` -- the shared error type for endpoint error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON license report
- [ ] Response body matches the shape: `{ groups: [{ license: string, packages: [...], compliant: bool }] }`
- [ ] Returns appropriate error (e.g., 404) when the SBOM ID does not exist
- [ ] Route is registered in the SBOM endpoint module's router

## Test Requirements
- [ ] Integration test: valid SBOM ID returns 200 with correct report structure
- [ ] Integration test: non-existent SBOM ID returns appropriate error status
- [ ] Integration test: SBOM with no packages returns 200 with empty groups array

## Verification Commands
- `cargo build` -- verify the project compiles with the new endpoint
- `cargo test` -- verify all tests pass including new integration tests

## Dependencies
- Depends on: Task 2 -- Implement license report service with transitive dependency resolution
