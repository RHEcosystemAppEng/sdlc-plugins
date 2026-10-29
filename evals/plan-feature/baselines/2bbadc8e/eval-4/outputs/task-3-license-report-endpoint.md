## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that returns a structured license compliance report for a given SBOM. This endpoint connects the license report service (Task 2) to the HTTP layer, handles route registration, and returns the report as JSON. This is the public API surface for the license compliance report feature (TC-9004).

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report` that extracts the SBOM ID from the path, loads the license policy, calls `LicenseReportService::generate_report()`, and returns the `LicenseReport` as JSON

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the license report route alongside existing SBOM routes (`/api/v2/sbom`)
- `server/src/main.rs` — Ensure the SBOM module routes (which now include the license report) are mounted (likely already handled by existing module mount)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report grouped by license type with compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the endpoint pattern established by existing SBOM endpoints: `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) and `modules/fundamental/src/sbom/endpoints/list.rs` (GET /api/v2/sbom). The handler should extract the SBOM ID from the path using Axum extractors, similar to the existing `get.rs` handler.
  Per CONVENTIONS.md: endpoint registration follows the pattern in `endpoints/mod.rs`; each module registers its routes and `server/main.rs` mounts all modules.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` endpoint file scope.
- Error handling: return `Result<Json<LicenseReport>, AppError>` following the existing pattern where all handlers return `Result<T, AppError>` with `.context()` wrapping. Reference `common/src/error.rs` for the AppError enum.
  Per CONVENTIONS.md: all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` file scope.
- Route registration: add the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` using the same router pattern as the existing `list` and `get` routes. The route should be nested under the existing `/api/v2/sbom` prefix.
- The license policy should be loaded from the configured JSON file path. Consider injecting the policy path via application state/config so it's testable.
- No pagination is needed for this endpoint — it returns the complete report in a single response (unlike list endpoints that use `PaginatedResults<T>`).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Reference implementation for a GET endpoint with path parameter extraction (`{id}`)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow for adding the new route
- `common/src/error.rs::AppError` — Error type implementing `IntoResponse` for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON body containing license groups
- [ ] Each license group contains: license name, list of packages, and compliant flag
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Returns appropriate error response for invalid SBOM ID format
- [ ] Route is registered and accessible alongside existing SBOM endpoints

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` returns 200 with expected JSON structure for a valid SBOM
- [ ] Integration test: returns 404 for a non-existent SBOM ID
- [ ] Integration test: response includes both compliant and non-compliant license groups when the SBOM contains packages with mixed license compliance

## Verification Commands
- `cargo build` — compiles without errors
- `cargo test` — all tests pass

## Dependencies
- Depends on: Task 2 — Add license report service with transitive dependency resolution
