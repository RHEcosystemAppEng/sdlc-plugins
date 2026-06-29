# Task 3 — Add license report REST endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that returns a structured license compliance report for a given SBOM. The endpoint calls the `LicenseReportService` to generate the report and returns it as JSON. Register the new route in the SBOM endpoint module and mount it in the server.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — add route registration for `GET /api/v2/sbom/{id}/license-report` pointing to the new handler
- `server/src/main.rs` — ensure the SBOM module routes (which now include the license-report sub-route) are mounted (likely already handled by existing SBOM route mounting)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — handler function for `GET /api/v2/sbom/{id}/license-report`; extracts the SBOM ID from the path, loads the license policy, calls `LicenseReportService::generate_report`, and returns `Json<LicenseReport>`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `{ groups: [{ license: "MIT", packages: [{ name: "...", version: "...", transitive: false }], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction and error handling
- Route registration should follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — add a `.route("/api/v2/sbom/:id/license-report", get(license_report_handler))` or equivalent Axum route definition
- The handler should load the `LicensePolicy` from the configured path (injected via Axum state/extension) and pass it to `LicenseReportService::generate_report`
- Return `Json<LicenseReport>` on success, following the same serialization pattern used by other SBOM endpoints
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages — consider query efficiency when joining across `sbom_package` and `package_license` tables
- Do not create any debug, admin, or internal/exec endpoints — only the license-report endpoint specified above

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM detail endpoint; follow its handler pattern for path extraction, service invocation, and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration; follow the same pattern for adding a new route
- `common/src/error.rs::AppError` — shared error handling; reuse for endpoint error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with the grouped license report JSON
- [ ] Request with a nonexistent SBOM ID returns 404
- [ ] Response JSON structure matches: `{ groups: [{ license: String, packages: [...], compliant: bool }] }`
- [ ] No authentication-bypassing or debug endpoints are created

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` returns 200 with correct report structure for an SBOM with known package-license data
- [ ] Integration test: `GET /api/v2/sbom/{nonexistent-id}/license-report` returns 404
- [ ] Integration test: report correctly flags non-compliant licenses based on the loaded policy
- [ ] Integration test: report includes transitive dependency packages

## Verification Commands
- `cargo test --test api license_report` — expected: all license report integration tests pass
- `curl -s http://localhost:8080/api/v2/sbom/{test-id}/license-report | jq .groups` — expected: JSON array of license groups with compliance flags

## Documentation Updates
- `README.md` — add license report endpoint to the API section if one exists

## Dependencies
- Depends on: Task 2 — Add license report model and service
