## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license compliance report service and REST endpoint for feature TC-9004. The service aggregates package license data for an SBOM, walks the transitive dependency tree, groups packages by license type, and flags non-compliant licenses using the configurable policy from Task 1. The endpoint exposes this as `GET /api/v2/sbom/{id}/license-report`. Integration tests verify the full request-response cycle.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with a method to generate a LicenseReport for a given SBOM ID: queries sbom_package and package_license entities, walks transitive dependencies, groups by license, checks compliance against LicensePolicy
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum GET handler for `/api/v2/sbom/{id}/license-report`, extracts SBOM ID from path, calls LicenseReportService, returns JSON response
- `tests/api/license_report.rs` — integration tests for the license report endpoint

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod license_report;` re-export
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/license-report` route in the SBOM router
- `server/src/main.rs` — verify sbom module route mounting includes the new sub-route (may not require changes if the sbom module router auto-includes sub-routes)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM. Response body: `{ groups: [{ license: "MIT", packages: [{ name: "serde", version: "1.0.0" }], compliant: true }] }`. Returns 404 if the SBOM ID does not exist.

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for database connection handling, dependency injection, and method signatures.
- Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction, service invocation, and JSON response construction.
- Query strategy for license aggregation:
  1. Use `sbom_package` entity to get all packages for the given SBOM ID
  2. Join with `package_license` entity to get the license for each package
  3. For transitive dependencies, follow package relationships recursively through the sbom_package join table
  4. Group results by license identifier
  5. For each group, check compliance against the LicensePolicy
- Use `common/src/db/query.rs` helpers for database query construction where applicable.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping for error messages.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern of existing routes (e.g., the `.route("/{id}", get(get::handler))` pattern but with `/{id}/license-report`).
- Performance: the query should be optimized for SBOMs with up to 1000 packages (p95 < 500ms). Consider using a single JOIN query rather than N+1 queries. If the dependency tree walk is expensive, consider limiting recursion depth or using a CTE.
- Do NOT create any new database tables — all data must be aggregated from existing `sbom_package` and `package_license` entities.
- Follow the integration test pattern from `tests/api/sbom.rs` for test setup, database fixtures, and response assertions. Use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Per repo Key Conventions (Endpoint registration): Register the route in the SBOM module's `endpoints/mod.rs`; `server/main.rs` mounts all modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per repo Key Conventions (Error handling): All handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust handler scope.
- Per repo Key Conventions (Testing): Integration tests in `tests/api/` hit a real PostgreSQL test database. Applies: task creates `tests/api/license_report.rs` matching the convention's test file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference for service struct pattern, database connection handling, and query execution
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for GET endpoint handler pattern with path parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages belonging to an SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for querying license data
- `common/src/error.rs::AppError` — error enum with IntoResponse implementation
- `tests/api/sbom.rs` — reference for integration test setup, fixtures, and assertion patterns

## Acceptance Criteria
- [ ] GET /api/v2/sbom/{id}/license-report returns HTTP 200 with packages grouped by license type
- [ ] Response format matches the specification: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- [ ] Packages with non-compliant licenses (per configured policy) are flagged with `compliant: false`
- [ ] Transitive dependency licenses are included in the report (not just direct dependencies)
- [ ] Report generation completes within p95 < 500ms for SBOMs with up to 1000 packages
- [ ] Returns HTTP 404 with appropriate error message when SBOM ID does not exist
- [ ] No new database tables are created — all data is aggregated from existing entities
- [ ] Route is correctly registered under the SBOM module's endpoint router

## Test Requirements
- [ ] Integration test: GET returns 200 with correctly grouped license data for an SBOM with multiple distinct licenses
- [ ] Integration test: Non-compliant licenses are correctly flagged with `compliant: false` based on the configured policy
- [ ] Integration test: Transitive dependencies are included in the report alongside direct dependencies
- [ ] Integration test: Returns 404 for a nonexistent SBOM ID
- [ ] Integration test: SBOM with no packages returns an empty groups array
- [ ] Integration test: SBOM where all packages have compliant licenses returns all groups with `compliant: true`

## Verification Commands
- `cargo test --test license_report` — all integration tests pass
- `cargo clippy -- -D warnings` — no lint warnings on new code

## Documentation Updates
- `README.md` — add the license report endpoint to the API endpoint listing

## Dependencies
- Depends on: Task 1 — Add license policy configuration and compliance report domain model
