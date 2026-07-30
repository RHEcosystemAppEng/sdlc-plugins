## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that returns a license compliance report for the specified SBOM. The endpoint delegates to the license report service (Task 2) and returns the grouped license data with compliance flags. This endpoint enables compliance officers to retrieve a structured report and CI/CD pipelines to use it as an automated compliance gate.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Endpoint handler function: extracts the SBOM ID path parameter, calls `LicenseReportService::generate_report`, and returns the `LicenseReport` as a JSON response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `GET /api/v2/sbom/{id}/license-report` route alongside existing SBOM endpoints (list, get)
- `server/src/main.rs` — Verify the SBOM module routes are already mounted (they should be); no changes expected unless the new sub-route requires explicit mounting

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a `LicenseReport` JSON response with structure `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`. Path parameter `id` is the SBOM UUID. Returns 404 if SBOM not found, 200 with report on success.

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction and error handling
- The handler function signature should follow: `async fn license_report(Path(id): Path<Uuid>, State(db): State<DatabaseConnection>) -> Result<Json<LicenseReport>, AppError>`
- Register the route in `endpoints/mod.rs` using the same pattern as existing routes (e.g., `.route("/:id/license-report", get(license_report))`)
- Return `AppError::NotFound` (or equivalent from `common/src/error.rs`) when the SBOM ID does not exist
- The endpoint should NOT use `PaginatedResults` — the license report is a single structured response, not a paginated list
- Per docs/constraints.md section 2 (Commit Rules): reference Jira issue ID in commit footer; use Conventional Commits format
- Per docs/constraints.md section 3 (PR Rules): branch named after Jira issue ID; post PR link as Jira comment
- Per docs/constraints.md section 5 (Code Change Rules): changes must be scoped to listed files; inspect code before modifying
- Per CONVENTIONS.md -- Framework: use Axum for HTTP routing and handler definitions. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` endpoint file scope.
- Per CONVENTIONS.md -- Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md -- Endpoint registration: register routes in `endpoints/mod.rs`; `server/main.rs` mounts all modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — established pattern for single-resource SBOM endpoint with path parameter extraction and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for the SBOM module
- `common/src/error.rs::AppError` — error type for 404 Not Found and other error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON `LicenseReport` for a valid SBOM ID
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Response structure matches `{ groups: [{ license: string, packages: [...], compliant: bool }] }`
- [ ] Endpoint is registered and accessible via the Axum router

## Test Requirements
- [ ] Integration test: GET request with valid SBOM ID returns 200 and correct report structure
- [ ] Integration test: GET request with non-existent SBOM ID returns 404
- [ ] Integration test: report response contains expected license groups with compliance flags

## Verification Commands
- `cargo test --test api license_report` — runs the license report integration tests
- `curl http://localhost:8080/api/v2/sbom/{id}/license-report` — manual endpoint verification

## Dependencies
- Depends on: Task 2 — Implement license report service
