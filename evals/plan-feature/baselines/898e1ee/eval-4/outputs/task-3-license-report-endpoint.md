## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that invokes the license report service method and returns the structured compliance report as JSON. Register the new route in the SBOM module's endpoint registration and ensure it is mounted by the server.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler function for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `license_report` route in the SBOM endpoint router

## Implementation Notes
Follow the existing endpoint patterns in the SBOM module. `modules/fundamental/src/sbom/endpoints/get.rs` demonstrates the convention for Axum handler functions: extracting path parameters, calling the service, and returning `Result<Json<T>, AppError>`.

The handler should:
1. Extract the SBOM `id` from the path using Axum's `Path` extractor
2. Call `SbomService::license_report(id)` from task 2
3. Return `Json(report)` on success
4. Propagate `AppError` on failure (the `AppError` enum in `common/src/error.rs` already implements `IntoResponse`)

Route registration in `modules/fundamental/src/sbom/endpoints/mod.rs` should add the new route alongside the existing `/api/v2/sbom/{id}` GET route. The existing `mod.rs` shows the pattern for declaring submodule handlers and adding them to the router.

The server's `main.rs` (`server/src/main.rs`) already mounts the SBOM module's routes, so no changes should be needed there unless the module's route registration pattern requires explicit addition.

Per CONVENTIONS.md §Error Handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Endpoint Registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing GET handler for SBOM details; follow the same pattern for path extraction, service invocation, and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow for adding the new endpoint
- `common/src/error.rs::AppError` — Error type that implements `IntoResponse`; reuse for error propagation

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON body matching the `LicenseReport` schema
- [ ] Response content type is `application/json`
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Route is registered and accessible without server changes beyond the SBOM module

## Test Requirements
- [ ] Handler returns 200 with correct JSON structure for a valid SBOM with license data
- [ ] Handler returns 404 for a non-existent SBOM ID

## Dependencies
- Depends on: Task 2 — Add license report service logic

[sdlc-workflow] Description digest: sha256-md:2a8eead6b677cf94e37e583db08e8ed2f5710eeccb1685213e8cf6c4edf247c8
