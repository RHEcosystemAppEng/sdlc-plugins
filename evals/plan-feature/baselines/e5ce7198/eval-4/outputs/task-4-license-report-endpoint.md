## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that returns a license compliance report for the specified SBOM. The endpoint invokes the LicenseReportService and returns the LicenseReport as a JSON response. This task also registers the new route in the SBOM module's endpoint configuration and mounts it in the server.

## Files to Create
- `modules/fundamental/src/license/endpoints/mod.rs` — route registration for the license report endpoint
- `modules/fundamental/src/license/endpoints/report.rs` — GET handler for the license report

## Files to Modify
- `modules/fundamental/src/license/mod.rs` — register the endpoints submodule
- `modules/fundamental/src/sbom/endpoints/mod.rs` — mount the license report route under `/api/v2/sbom/{id}/license-report`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a LicenseReport JSON response with packages grouped by license and compliance flags

## Implementation Notes
Follow the existing endpoint patterns from `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/advisory/endpoints/get.rs` for handler structure. The handler should:

1. Extract the SBOM ID from the path parameter
2. Inject the LicenseReportService via Axum's state/extension mechanism
3. Call the service to generate the report
4. Return the LicenseReport as `Json<LicenseReport>` with `StatusCode::OK`
5. Map service errors to appropriate HTTP status codes via AppError's IntoResponse implementation

Register the route in the SBOM endpoints module (`modules/fundamental/src/sbom/endpoints/mod.rs`) since it is logically a sub-resource of SBOM. The route pattern should match existing nested resource patterns.

Per CONVENTIONS.md §Endpoint Registration: each module's endpoints/mod.rs registers routes; server/main.rs mounts all modules.
Applies: task creates `modules/fundamental/src/license/endpoints/mod.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler pattern for SBOM detail endpoint
- `common/src/error.rs::AppError` — automatic error-to-HTTP-response mapping via IntoResponse

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid LicenseReport JSON body
- [ ] Response Content-Type is application/json
- [ ] Non-existent SBOM ID returns 404 with appropriate error message
- [ ] Invalid SBOM ID format returns 400
- [ ] Endpoint is reachable and correctly mounted in the Axum router

## Test Requirements
- [ ] Handler test: valid SBOM ID returns 200 with expected JSON structure
- [ ] Handler test: non-existent SBOM ID returns 404
- [ ] Handler test: response includes groups array and summary object

## Dependencies
- Depends on: Task 3 — License report service

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}
