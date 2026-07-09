## Repository
trustify-backend

## Target Branch
main

## Description
Wire up the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that invokes the license report service (Task 2) and returns the structured compliance report as JSON. Register the new route in the SBOM endpoint module following the established endpoint registration pattern.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Implement the Axum handler function for `GET /api/v2/sbom/{id}/license-report`; extract SBOM ID from path, call `LicenseReportService::generate_report`, return JSON response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/api/v2/sbom/{id}/license-report` route in the existing SBOM route builder

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }], total_packages: N, compliant_count: N, non_compliant_count: N }`

## Implementation Notes
- Follow the existing endpoint pattern from `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure: extract path parameters with `Path<SbomId>`, inject service dependencies, return `Result<Json<LicenseReport>, AppError>`
- The handler should load the license policy configuration (from a configured path or application state) and pass it to the `LicenseReportService`
- Return HTTP 404 if the SBOM ID does not exist, consistent with the existing `get.rs` endpoint behavior
- Per CONVENTIONS.md Key Conventions (Error Handling): the handler must return `Result<T, AppError>` with `.context()` wrapping on all fallible operations.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md Key Conventions (Endpoint Registration): register the route in `endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs`. The route should be `.route("/api/v2/sbom/{id}/license-report", get(license_report))` or equivalent.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md Key Conventions (Framework): use Axum extractors (`Path`, `State`, `Json`) consistent with existing endpoint implementations.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET handler; follow its pattern for path extraction, service invocation, and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration pattern to follow
- `common/src/error.rs::AppError` — standard error type for handler return values

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON body containing grouped license data and compliance flags
- [ ] `GET /api/v2/sbom/{nonexistent-id}/license-report` returns HTTP 404
- [ ] Response content type is `application/json`
- [ ] Route is registered and accessible at the documented path

## Test Requirements
- [ ] Verify the endpoint returns the correct JSON structure with license groups
- [ ] Verify 404 is returned for a nonexistent SBOM ID
- [ ] Verify the response includes compliance flags per group

## Verification Commands
- `cargo build` — full project compiles without errors
- `curl http://localhost:8080/api/v2/sbom/{id}/license-report` — returns JSON license report (requires running server and valid SBOM ID)

## Dependencies
- Depends on: Task 2 — Add license report model and service
