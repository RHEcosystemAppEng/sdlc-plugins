## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service that aggregates package-license data from existing database tables, walks the full dependency tree for transitive dependencies, and checks each license against the configurable policy. This service is the core business logic for the SBOM license compliance report feature (TC-9004). It must aggregate from existing package-license data without creating new database tables, and meet the p95 < 500ms performance target for SBOMs with up to 1000 packages.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with methods: `generate_report(sbom_id, policy) -> Result<LicenseReport, AppError>` that queries package-license data, walks transitive dependencies, groups by license, and flags compliance

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module

## API Changes
- `LicenseReportService::generate_report(sbom_id: Uuid, policy: &LicensePolicy) -> Result<LicenseReport, AppError>` — NEW: generates license compliance report for a given SBOM

## Implementation Notes
- Follow the service pattern established by `modules/fundamental/src/sbom/service/sbom.rs` (SbomService). The new `LicenseReportService` should mirror the same constructor, dependency injection, and error handling patterns.
  Per CONVENTIONS.md: follow the existing service pattern with `Result<T, AppError>` and `.context()` error wrapping.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` service file scope.
- Query package-license data using SeaORM via the existing entities: `entity/src/sbom_package.rs` (SBOM-Package join), `entity/src/package.rs` (Package), and `entity/src/package_license.rs` (Package-License mapping). No new database tables should be created.
- For transitive dependency walking: traverse the full dependency tree starting from the SBOM's direct packages, following package relationships in `sbom_package` to resolve all transitive dependencies. Use an iterative BFS/DFS approach with cycle detection to handle circular dependencies.
- Use `common/src/db/query.rs` query builder helpers for constructing efficient database queries. Consider batch loading package-license mappings to avoid N+1 query patterns and meet the p95 < 500ms target.
  Per CONVENTIONS.md: use shared query builder helpers from `common/src/db/query.rs` for filtering, pagination, and sorting.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` file scope.
- Group packages by license type and apply `LicensePolicy::check_compliance()` from Task 1 to set the `compliant` flag on each group.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Reference implementation for service pattern (constructor, database access, error handling)
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Existing package query logic that can inform how to query package data efficiently
- `common/src/db/query.rs` — Shared query builder helpers for constructing database queries with filtering and pagination
- `entity/src/package_license.rs` — Existing Package-License mapping entity for querying license data
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for resolving packages belonging to an SBOM

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report()` returns a `LicenseReport` with packages grouped by license type
- [ ] Each `LicenseGroup` has a correct `compliant` flag based on the license policy
- [ ] Transitive dependencies are included in the report (not just direct packages)
- [ ] No new database tables are created — all data is aggregated from existing entities
- [ ] Circular dependencies in the package tree are handled without infinite loops
- [ ] Report generation completes within 500ms for SBOMs with up to 1000 packages (p95)

## Test Requirements
- [ ] Unit test: service correctly groups packages by license type
- [ ] Unit test: service flags non-compliant licenses based on a test policy
- [ ] Unit test: service includes transitive dependencies in the report
- [ ] Unit test: service handles circular dependencies without hanging
- [ ] Unit test: service returns an error when the SBOM ID does not exist
- [ ] Performance test: service generates a report for a 1000-package SBOM within 500ms

## Verification Commands
- `cargo build` — compiles without errors
- `cargo test --lib` — all unit tests pass

## Dependencies
- Depends on: Task 1 — Add license report model and policy configuration
