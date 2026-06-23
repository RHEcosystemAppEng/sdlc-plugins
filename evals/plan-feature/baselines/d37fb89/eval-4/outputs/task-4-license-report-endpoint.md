## Repository
trustify-backend

## Target Branch
main

## Description
Wire up the HTTP endpoint for the license compliance report. Register `GET /api/v2/sbom/{id}/license-report` as a new route in the SBOM module's endpoint configuration, implementing the handler that calls the license report service and returns the structured JSON response.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/license-report` route in the SBOM router
- `modules/fundamental/src/sbom/mod.rs` — Ensure endpoint module exports are up to date

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a `LicenseReport` JSON response with packages grouped by license and compliance flags

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for the handler structure:
- Extract the SBOM `id` from the path using Axum's `Path` extractor
- Call `SbomService::generate_license_report()` from the service layer
- Return `Result<Json<LicenseReport>, AppError>` matching the codebase's error handling convention
- Use `.context()` wrapping on service calls per `common/src/error.rs` patterns

Route registration in `modules/fundamental/src/sbom/endpoints/mod.rs` should follow the existing pattern for `list.rs` and `get.rs` — add the new handler to the SBOM router at the nested path `/{id}/license-report`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing `GET /api/v2/sbom/{id}` handler; follow the same Axum extractor and response patterns
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration pattern to follow for adding the new route

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` is registered and reachable
- [ ] Handler extracts SBOM ID from path and calls the license report service
- [ ] Response is `200 OK` with `Content-Type: application/json` containing the `LicenseReport` structure
- [ ] Non-existent SBOM ID returns `404 Not Found` with appropriate error body
- [ ] Error responses follow the `AppError` format used by other endpoints

## Test Requirements
- [ ] Handler returns 200 with valid license report JSON for a valid SBOM ID
- [ ] Handler returns 404 for a non-existent SBOM ID
- [ ] Response JSON structure matches `{ "sbom_id": "...", "groups": [...], "total_packages": N, "non_compliant_count": N }`

## Dependencies
- Depends on: Task 3 — Implement license report service with transitive dependency resolution

[sdlc-workflow] Description digest: sha256-md:6e448ee557b149960036760a0a3fd7cfe666ba23516f69cc74e83dc9ad743c86
