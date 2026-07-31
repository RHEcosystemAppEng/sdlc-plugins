## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` REST endpoint that returns a license compliance report for a given SBOM. The endpoint delegates to the LicenseReportService (Task 2) and returns the LicenseReport as a JSON response. This endpoint enables compliance teams and CI/CD pipelines to retrieve a structured license audit in a single API call.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler function for the license report endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/license-report` route in the SBOM route builder

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a license compliance report grouped by license type with compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — extract path parameters using Axum's `Path<Uuid>` extractor, call the service, and return the result as JSON.
- Per Key Conventions §Module pattern: follow the `model/ + service/ + endpoints/` structure. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's endpoints directory scope.
- Per Key Conventions §Error handling: the handler must return `Result<Json<LicenseReport>, AppError>` with `.context()` wrapping for service errors. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` which is a handler returning `Result<T, AppError>`.
- Per Key Conventions §Endpoint registration: register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern as the existing `list.rs` and `get.rs` route registrations. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- The endpoint path should be nested under the existing SBOM routes: add `.route("/{id}/license-report", get(license_report::handler))` to the SBOM router in `endpoints/mod.rs`.
- No new database tables are needed — the service aggregates from existing package-license data.
- Consider adding `tower-http` caching headers for the response per Key Conventions §Caching, since license reports for a given SBOM are deterministic and can be cached.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM get handler; follow the same pattern for path parameter extraction and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration; add the license-report route alongside existing routes
- `common/src/error.rs::AppError` — error type for handler return values

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON license compliance report for a valid SBOM ID
- [ ] Response body matches the expected shape: `{ groups: [{ license: string, packages: [...], compliant: boolean }] }`
- [ ] Endpoint returns HTTP 404 for a non-existent SBOM ID
- [ ] Route is registered in the SBOM endpoint module and accessible via the API

## Test Requirements
- [ ] Integration test: endpoint returns 200 with correct report structure for a valid SBOM
- [ ] Integration test: endpoint returns 404 for non-existent SBOM
- [ ] Integration test: report correctly groups packages by license
- [ ] Integration test: report correctly flags non-compliant licenses

## Verification Commands
- `cargo test --test api -- license_report` — runs the license report integration tests
- `curl http://localhost:8080/api/v2/sbom/{id}/license-report` — manual endpoint verification

## Dependencies
- Depends on: Task 1 — Add license policy configuration and license report models
- Depends on: Task 2 — Add license report service with transitive dependency resolution
