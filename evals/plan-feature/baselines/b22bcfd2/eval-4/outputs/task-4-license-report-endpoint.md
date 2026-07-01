## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that generates and returns a license compliance report for a given SBOM. This wires the LicenseReportService into the Axum HTTP layer and registers the route.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler function `async fn get_license_report(Path(id): Path<Uuid>, State(state): State<AppState>) -> Result<Json<LicenseReport>, AppError>` that loads the license policy, calls `LicenseReportService::generate_report()`, and returns the JSON response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `mod license_report;` and register the new route `GET /api/v2/sbom/{id}/license-report` in the router builder
- `server/src/main.rs` — Ensure the license policy config is loaded at startup and available in the application state (if not already handled by existing config loading)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM, with packages grouped by license and compliance flags based on the configured policy

## Implementation Notes
Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` for the handler signature and `modules/fundamental/src/sbom/endpoints/mod.rs` for route registration. Use Axum's `Path` extractor for the SBOM ID and `State` extractor for shared application state. Return `Result<Json<LicenseReport>, AppError>` to match the codebase's error handling convention. Load the `LicensePolicy` from application state (configured at startup from `config/default-license-policy.json`). The response should have HTTP 200 on success and appropriate error codes (404 for unknown SBOM ID, 500 for internal errors).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Handler pattern for SBOM-scoped endpoints with Path extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern
- `common/src/error.rs::AppError` — Error type implementing IntoResponse

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON LicenseReport body for a valid SBOM
- [ ] Returns HTTP 404 when the SBOM ID does not exist
- [ ] Response JSON matches the schema: `{ sbom_id, generated_at, groups: [{ license, packages, compliant }], summary }`
- [ ] No new backdoor, debug, or admin endpoints are created

## Test Requirements
- [ ] Integration test: GET license-report for a valid SBOM returns 200 with expected structure
- [ ] Integration test: GET license-report for nonexistent SBOM returns 404
- [ ] Integration test: response includes packages grouped by license with correct compliance flags

## Dependencies
- Depends on: Task 3 — License report service (uses LicenseReportService)
