# Task 2 — Create license report model structs and service with transitive dependency resolution

## Repository
trustify-backend

## Target Branch
main

## Description
Create the model structs and service logic for the license compliance report. The service aggregates license data from all packages in an SBOM (including transitive dependencies), groups packages by license type, and checks each group's compliance against the license policy from Task 1.

The service walks the full dependency tree via the `sbom_package` join table to include transitive dependencies, then queries the `package_license` entity to map each package to its license(s). Packages are grouped by license identifier, and each group is annotated with a compliance flag based on the configured license policy.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Model structs: `LicenseReport` (top-level response with `groups` array), `LicenseGroup` (license identifier, list of packages, `compliant` boolean)
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` implementing: SBOM package enumeration with transitive dependency traversal, license aggregation from `package_license` entity, policy compliance evaluation

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` module declaration
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` module declaration

## API Changes
- Internal service API (not a REST endpoint — that is Task 3):
  - `LicenseReportService::generate(db: &DatabaseConnection, sbom_id: Id, policy: &LicensePolicy) -> Result<LicenseReport, AppError>` — NEW

## Implementation Notes
- Follow the established module pattern: `model/` for data types, `service/` for business logic. See `modules/fundamental/src/sbom/model/summary.rs` for the model struct pattern and `modules/fundamental/src/sbom/service/sbom.rs` for the service pattern.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's Rust module scope.
- Use SeaORM to query the `sbom_package` and `package_license` entities. Reference `entity/sbom_package.rs` for the SBOM-to-package relationship and `entity/package_license.rs` for the package-to-license mapping.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` file scope.
- For transitive dependency traversal: query all packages linked to the SBOM via `sbom_package`, then recursively resolve their dependencies. The `sbom_package` join table provides the package membership for each SBOM.
- Per project conventions (§Error handling): the service must return `Result<LicenseReport, AppError>` with `.context()` wrapping on all database query failures. See `common/src/error.rs` for the `AppError` definition.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` file scope.
- The `LicenseReport` response struct should serialize to: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }` as specified in the feature requirements.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use batch queries rather than N+1 patterns — load all package-license mappings in a single query and group in-memory.
- Per project conventions (§Response types): this is not a list/paginated endpoint, so do not use `PaginatedResults<T>`. The response is a single `LicenseReport` object.
- No new database tables per NFR — aggregate from existing `package_license` data.

## Reuse Candidates
- `entity/package_license.rs::PackageLicense` — Existing entity for package-to-license mapping; use for license data queries
- `entity/sbom_package.rs::SbomPackage` — Existing entity for SBOM-to-package relationship; use for dependency tree traversal
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Existing package model with license field; reference for package data shape
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Existing package service; reference for SeaORM query patterns
- `common/src/db/query.rs` — Shared query builder helpers for filtering and sorting
- `common/src/error.rs::AppError` — Error type with `.context()` wrapping pattern

## Acceptance Criteria
- [ ] `LicenseReport` and `LicenseGroup` structs serialize to the expected JSON shape
- [ ] Service correctly aggregates all packages in an SBOM grouped by license
- [ ] Service includes transitive dependency licenses (walks the full dependency tree)
- [ ] Each license group has a `compliant` flag based on the license policy
- [ ] Service returns appropriate `AppError` when SBOM ID is not found
- [ ] No new database tables are created

## Test Requirements
- [ ] Unit test: verify `LicenseReport` JSON serialization matches expected format
- [ ] Unit test: verify license grouping logic with multiple packages under the same license
- [ ] Unit test: verify compliance flag is set correctly for allowed, denied, and default-disposition licenses
- [ ] Unit test: verify transitive dependency packages are included in the report
- [ ] Unit test: verify error handling for non-existent SBOM ID

## Verification Commands
- `cargo build -p fundamental` — compiles without errors
- `cargo test -p fundamental` — all tests pass

## Dependencies
- Depends on: Task 1 — Add license policy configuration file and loader
