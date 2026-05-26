# Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Register the license compliance report endpoint at `GET /api/v2/sbom/{id}/license-report`. This endpoint accepts an SBOM ID, invokes the `LicenseReportService` to generate the report, and returns the structured `LicenseReport` JSON response. This is the user-facing entry point for the license compliance feature.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add route registration for `GET /api/v2/sbom/{id}/license-report`, following the existing pattern for route mounting in this file.
- `server/src/main.rs` — If the SBOM module's endpoint registration does not automatically include the new route, add any needed wiring here. Inspect to confirm whether changes are needed.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Handler function for the license report endpoint. Extracts `id` from the path, loads the license policy, calls `LicenseReportService::generate`, and returns the `LicenseReport` as JSON. Returns appropriate HTTP error codes (404 for nonexistent SBOM, 500 for internal errors).

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM. Response shape: `{ "groups": [{ "license": "MIT", "packages": [{ "name": "...", "version": "...", "transitive": false }], "compliant": true }] }`.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/` — see `get.rs` for how the `GET /api/v2/sbom/{id}` handler extracts the path parameter, calls the service, and returns a JSON response with proper error handling.
- Use `axum::extract::Path` for the `{id}` parameter, matching the pattern in `get.rs`.
- Return `Result<Json<LicenseReport>, AppError>` from the handler, consistent with other endpoint handlers.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing `.route()` pattern used for `/api/v2/sbom` and `/api/v2/sbom/{id}`.
- The license policy should be loaded once (ideally at server startup and injected via Axum state), not per-request. Inspect `server/src/main.rs` to see how other services are initialized and shared.
- Per docs/constraints.md §5.2: inspect existing code before implementing. Review the endpoint registration in `modules/fundamental/src/sbom/endpoints/mod.rs` and the server setup in `server/src/main.rs`.
- Per docs/constraints.md §5.8: compare with sibling endpoint implementations (`get.rs`, `list.rs`) for parity on error handling, logging, and response patterns.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — sibling endpoint handler showing path extraction, service invocation, and JSON response pattern.
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow.
- `common/src/error.rs::AppError` — error handling with `IntoResponse` implementation.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with the license compliance report JSON
- [ ] Response matches the specified shape: `{ "groups": [...] }` with license, packages, and compliant fields
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Returns appropriate error (500) when the license policy file is missing or malformed
- [ ] Endpoint is accessible via the same authentication/authorization as other SBOM endpoints

## Test Requirements
- [ ] Integration test: call the endpoint for an SBOM with known license data and verify the response structure and compliance flags
- [ ] Integration test: call the endpoint for a nonexistent SBOM ID and verify 404 response
- [ ] Integration test: verify the endpoint returns packages grouped by license with correct counts

## Documentation Updates
- `README.md` — Add the new license report endpoint to any API endpoint listing or feature documentation

## Dependencies
- Depends on: Task 3 — Implement license report service with transitive dependency resolution
