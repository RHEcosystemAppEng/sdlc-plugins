## Repository
trustify-backend

## Target Branch
main

## Description
Add a REST endpoint `GET /api/v2/sbom/{id}/license-report` that returns a license compliance report for the specified SBOM. The endpoint invokes the LicenseReportService, loads the license policy configuration, and returns the grouped license report as JSON. This endpoint enables compliance officers and CI/CD pipelines to programmatically audit license compliance for any ingested SBOM.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the new `/api/v2/sbom/{id}/license-report` route in the existing SBOM route builder
- `modules/fundamental/Cargo.toml` -- add any new dependencies required for the endpoint (if any)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- handler function `get_license_report(Path(id): Path<Uuid>, State(state): State<AppState>) -> Result<Json<LicenseReport>, AppError>` that: (1) loads the LicensePolicy from the configured path, (2) calls LicenseReportService::generate_report, (3) returns the LicenseReport as JSON

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: returns a license compliance report for the specified SBOM. Response shape: `{ groups: [{ license: "MIT", packages: [{ name: "serde", version: "1.0.0", purl: "pkg:cargo/serde@1.0.0" }], compliant: true }] }`. Returns 404 if SBOM not found.

## Implementation Notes
- Per Key Conventions "Endpoint registration": register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern as `list.rs` and `get.rs`. The route should be `.route("/{id}/license-report", get(license_report::get_license_report))`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration file scope.
- Per Key Conventions "Error handling": the handler returns `Result<Json<LicenseReport>, AppError>` with `.context()` wrapping on all fallible operations.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust source file scope.
- Per Key Conventions "Caching": consider adding `tower-http` caching middleware to the license report route with an appropriate TTL, since license data changes infrequently. Follow the cache configuration pattern used in existing endpoint route builders.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder scope.
- Per Key Conventions "Module pattern": follow the `model/ + service/ + endpoints/` structure. The endpoint file goes alongside existing endpoint files.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's module endpoint file scope.
- Use utoipa annotations on the handler function for OpenAPI documentation generation, following the pattern of existing endpoint handlers.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- existing GET /api/v2/sbom/{id} handler; follow its pattern for path parameter extraction, state access, and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- existing route registration file; follow its pattern for adding new routes
- `common/src/error.rs::AppError` -- application error enum implementing IntoResponse; used by all endpoint handlers

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON LicenseReport body when the SBOM exists
- [ ] The response groups packages by license with `compliant` flags based on the configured policy
- [ ] Returns 404 with an appropriate error message when the SBOM ID does not exist
- [ ] The endpoint is registered in the SBOM route builder and accessible via the API
- [ ] OpenAPI schema includes the new endpoint with request/response documentation

## Test Requirements
- [ ] Integration test: GET /api/v2/sbom/{id}/license-report returns 200 with grouped license data for a valid SBOM
- [ ] Integration test: GET /api/v2/sbom/{id}/license-report returns 404 for a non-existent SBOM ID
- [ ] Integration test: response JSON matches the expected schema with groups, packages, and compliant fields

## Verification Commands
- `cargo test --test api license_report` -- runs the license report integration tests; expect all tests to pass
- `cargo run & curl -s http://localhost:8080/api/v2/sbom/{test-id}/license-report | jq .` -- verify the endpoint returns properly formatted JSON with license groups

## Dependencies
- Depends on: Task 1 -- Add license policy configuration and compliance report model
- Depends on: Task 2 -- Add license report service with transitive dependency traversal
