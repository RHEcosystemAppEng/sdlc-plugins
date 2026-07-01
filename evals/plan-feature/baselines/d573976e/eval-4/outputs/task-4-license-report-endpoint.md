# Task 4 — Add license report REST endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint `GET /api/v2/sbom/{id}/license-report` that returns a structured license compliance report for the specified SBOM. The endpoint delegates to the license report service and returns the report as JSON. This is the primary entry point for compliance teams and CI/CD pipelines to retrieve license audit data.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the license-report route alongside existing SBOM routes
- `server/src/main.rs` — no changes expected if route registration is modular (verify during implementation)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — handler function for GET /api/v2/sbom/{id}/license-report

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `LicenseReportSummary` as JSON (200 OK), or error responses (404 for unknown SBOM, 500 for internal errors)

## Implementation Notes
- Follow the existing endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) and `modules/fundamental/src/sbom/endpoints/list.rs` (GET /api/v2/sbom)
- Route registration: add the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing pattern for `/api/v2/sbom` routes
- Handler signature should follow the Axum pattern:
  ```rust
  async fn get_license_report(
      Path(id): Path<Uuid>,
      State(service): State<SbomService>,
  ) -> Result<Json<LicenseReportSummary>, AppError>
  ```
- The handler loads the license policy (from configuration or default), calls `SbomService::get_license_report()`, and returns the result as JSON
- Error handling: return 404 when the SBOM is not found, per the pattern in `common/src/error.rs::AppError`
- Consider adding `tower-http` caching headers for the report response, following the caching middleware pattern documented in the key conventions

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — follow handler pattern for GET /api/v2/sbom/{id}
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — error response handling with IntoResponse

## Acceptance Criteria
- [ ] GET /api/v2/sbom/{id}/license-report returns 200 with correct JSON response shape
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Response content-type is application/json
- [ ] Endpoint is registered and accessible at the correct path

## Test Requirements
- [ ] Integration test: call endpoint for a valid SBOM with known licenses and verify response shape and grouping
- [ ] Integration test: call endpoint for non-existent SBOM and verify 404 response
- [ ] Integration test: verify response includes compliance flags matching the configured policy
- [ ] Integration test: verify response includes transitive dependency licenses
- [ ] Integration test: verify response for SBOM with no packages returns empty groups array

## Verification Commands
- `cargo test --package fundamental -- license_report` — run license report tests
- `curl -s http://localhost:8080/api/v2/sbom/{id}/license-report | jq .` — manual verification of endpoint response

## Documentation Updates
- `README.md` — add license report endpoint to API documentation or endpoint listing
- API documentation (if OpenAPI spec exists) — add GET /api/v2/sbom/{id}/license-report schema

## Dependencies
- Depends on: Task 3 — Add license report service
