## Repository
trustify-backend

## Target Branch
main

## Description
Wire up the `GET /api/v2/sbom/{id}/license-report` endpoint that serves the license compliance report. The endpoint accepts an SBOM ID as a path parameter, loads the license policy, generates the report via `LicenseReportService`, and returns the structured JSON response.

## Files to Create
- `modules/fundamental/src/license/endpoints/mod.rs` — Route registration for the license report endpoint
- `modules/fundamental/src/license/endpoints/report.rs` — Handler for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/license/mod.rs` — add `endpoints` submodule declaration
- `modules/fundamental/src/sbom/endpoints/mod.rs` — mount the license report route under the SBOM route prefix
- `server/src/main.rs` — register the license module routes if needed

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `LicenseComplianceReport` JSON with packages grouped by license and compliance flags

## Implementation Notes
Follow the endpoint pattern from `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction and response handling. The handler should:

1. Extract `sbom_id` from the path using Axum's `Path` extractor
2. Load the license policy from the configured path (or use a default policy)
3. Call `LicenseReportService::generate_report(sbom_id, &policy)`
4. Return the `LicenseComplianceReport` as JSON with `StatusCode::OK`
5. Return `AppError` (404) if the SBOM ID does not exist

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing SBOM endpoints, following the route registration pattern used for `list.rs` and `get.rs`.

Per CONVENTIONS.md §Endpoint registration: register routes in `endpoints/mod.rs` and mount via `server/main.rs`.
Applies: task creates `modules/fundamental/src/license/endpoints/mod.rs` matching the convention's Rust file scope.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/license/endpoints/report.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference implementation for path parameter extraction and single-resource endpoint pattern
- `common/src/error.rs::AppError` — error type for handler responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid `LicenseComplianceReport` JSON body
- [ ] Returns 404 for non-existent SBOM IDs
- [ ] Route is registered and accessible when the server starts
- [ ] Response content type is `application/json`

## Test Requirements
- [ ] Integration test: valid SBOM ID returns 200 with expected report structure
- [ ] Integration test: non-existent SBOM ID returns 404

## Dependencies
- Depends on: Task 3 — License report service
