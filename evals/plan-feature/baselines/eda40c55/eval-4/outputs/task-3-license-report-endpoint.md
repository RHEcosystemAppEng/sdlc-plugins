## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that exposes the license report service to API consumers. The endpoint loads the license policy configuration, invokes the report service, and returns the structured compliance report as JSON. This is the API surface that compliance officers and CI/CD pipelines will call.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for GET /api/v2/sbom/{id}/license-report that loads the license policy, calls the report service, and returns the LicenseReport as JSON

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the license report route alongside existing SBOM endpoints

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `{ groups: [{ license: "MIT", packages: [{ name: "...", version: "...", purl: "..." }], compliant: true }] }` with status 200 on success, 404 if the SBOM ID is not found, 500 on internal error

## Implementation Notes
- Create an async Axum handler function `license_report` with signature:
  ```rust
  async fn license_report(
      Path(id): Path<Uuid>,
      State(state): State<AppState>,
  ) -> Result<Json<LicenseReport>, AppError>
  ```
- Load the license policy from a configured path (e.g., via AppState or environment variable)
- Call `LicenseReportService::generate_report(&state.db, id, &policy).await`
- Return `Json(report)` on success
- Return appropriate HTTP status codes: 404 for unknown SBOM ID, 500 for internal errors
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure, path extraction, and error handling
- Register the route in `endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs`:
  ```rust
  .route("/api/v2/sbom/:id/license-report", get(license_report::license_report))
  ```
- Per CONVENTIONS.md: endpoint registration pattern — register in the module's `endpoints/mod.rs`; `server/main.rs` mounts all modules.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint registration scope.
- Per CONVENTIONS.md: all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` error handling scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET /api/v2/sbom/{id} handler; follow its pattern for path parameter extraction, state access, and error response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — error type implementing IntoResponse for consistent HTTP error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns a 200 response with the license report JSON
- [ ] Response body matches the schema: `{ groups: [{ license, packages, compliant }] }`
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Returns appropriate error response on internal failures
- [ ] Endpoint is registered and reachable at the correct path

## Test Requirements
- [ ] Integration test: call the endpoint with a valid SBOM ID and verify 200 response with correct report structure
- [ ] Integration test: call the endpoint with a non-existent SBOM ID and verify 404 response
- [ ] Integration test: verify response content type is application/json

## Verification Commands
- `cargo test --test api -- license_report` — run the license report integration tests
- `curl http://localhost:8080/api/v2/sbom/{id}/license-report` — manually verify the endpoint returns a valid response

## Dependencies
- Depends on: Task 1 — Add license policy configuration model
- Depends on: Task 2 — Add license report model and service
