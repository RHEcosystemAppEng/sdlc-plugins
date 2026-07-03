## Repository

trustify-backend

## Target Branch

main

## Description

Wire up the `GET /api/v2/sbom/{id}/license-report` endpoint that exposes the license compliance report service. This endpoint follows the existing route registration and handler patterns in the SBOM module and returns the structured license report as JSON.

## Files to Modify

- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new license report route alongside existing SBOM routes (`/api/v2/sbom`)

## Files to Create

- `modules/fundamental/src/sbom/endpoints/license_report.rs` — handler function for `GET /api/v2/sbom/{id}/license-report`

## Implementation Notes

- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction and response formatting
- The handler should extract the SBOM ID from the path using Axum's `Path` extractor, and the `LicensePolicyService` from Axum's `Extension` extractor
- Call `generate_license_report` from the service layer (Task 3) and return the `LicenseReport` as `Json<LicenseReport>`
- Return `AppError` on failure, following the error handling pattern in `common/src/error.rs` — return 404 if the SBOM ID does not exist
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern used for the existing `get.rs` and `list.rs` routes
- No caching is required for the initial implementation; cache headers can be added later if performance monitoring indicates a need
- The endpoint requires authentication consistent with other `/api/v2/sbom` endpoints (no special auth bypass)

## Acceptance Criteria

- `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON body matching the `LicenseReport` structure
- The endpoint returns HTTP 404 when the SBOM ID does not exist
- The route is registered alongside existing SBOM routes in the endpoint module
- The endpoint follows existing authentication and error handling patterns
- `cargo check` passes with no errors

## Test Requirements

- Integration test in `tests/api/` verifying a successful license report response for an SBOM with known package/license data
- Integration test verifying 404 response for a non-existent SBOM ID
- Integration test verifying the response structure matches the expected JSON schema (groups array with license, packages, compliant fields)
