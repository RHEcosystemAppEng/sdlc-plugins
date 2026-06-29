# Task 2 — Add license report model and service

## Repository
trustify-backend

## Target Branch
main

## Description
Create the license report model structs and a service that aggregates package-license data from existing database tables, walks transitive dependencies via the SBOM-package graph, and evaluates each package's license against the configured policy. The service produces a structured report grouped by license type with compliance flags.

## Files to Modify
- `modules/fundamental/src/sbom/mod.rs` — add `pub mod license_report;` submodule declaration
- `modules/fundamental/Cargo.toml` — add dependency on `common` crate if not already present (for `LicensePolicy` access)

## Files to Create
- `modules/fundamental/src/sbom/license_report/mod.rs` — re-exports for model and service submodules
- `modules/fundamental/src/sbom/license_report/model.rs` — `LicenseReportGroup` struct (`license: String`, `packages: Vec<PackageLicenseEntry>`, `compliant: bool`) and `LicenseReport` struct (`groups: Vec<LicenseReportGroup>`); `PackageLicenseEntry` struct (`name: String`, `version: String`, `transitive: bool`)
- `modules/fundamental/src/sbom/license_report/service.rs` — `LicenseReportService` with a `generate_report(sbom_id: &str, policy: &LicensePolicy, db: &DatabaseConnection) -> Result<LicenseReport, AppError>` method

## Implementation Notes
- Follow the existing module pattern: each domain module uses `model/ + service/ + endpoints/` structure, as seen in `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/`
- The service must walk transitive dependencies by traversing the `sbom_package` join table (entity defined in `entity/src/sbom_package.rs`) and then resolving each package's license from the `package_license` mapping (entity in `entity/src/package_license.rs`)
- Use SeaORM queries following the patterns in existing services like `SbomService` (`modules/fundamental/src/sbom/service/sbom.rs`) and `PackageService` (`modules/fundamental/src/package/service/mod.rs`)
- Group packages by their license string, then check each group's license against `LicensePolicy::is_compliant` to set the `compliant` flag
- Mark packages as `transitive: true` when they are not direct dependencies of the SBOM (i.e., they are reached through the dependency tree rather than being top-level SBOM packages)
- All handlers return `Result<T, AppError>` with `.context()` wrapping per the existing error handling pattern in `common/src/error.rs`

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service for SBOM fetch/list operations; follow its query patterns and error handling style
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package service; reuse its query patterns for package-license lookups
- `entity/src/package_license.rs` — existing entity for package-license mapping; use for querying license data
- `entity/src/sbom_package.rs` — existing SBOM-package join table entity; use for walking the dependency graph
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `LicenseReport` contains groups sorted by license name, each with the list of packages using that license
- [ ] Each group has a `compliant` flag reflecting the policy evaluation
- [ ] Transitive dependencies are included and marked with `transitive: true`
- [ ] Report generation for a nonexistent SBOM ID returns an appropriate error
- [ ] No new database tables are created — all data is aggregated from existing `package_license` and `sbom_package` tables

## Test Requirements
- [ ] Unit test: report groups packages correctly by license type
- [ ] Unit test: `compliant` flag is `false` when the license is in the denied list
- [ ] Unit test: `compliant` flag is `true` when the license is in the allowed list
- [ ] Unit test: transitive dependencies are included and marked appropriately
- [ ] Unit test: empty SBOM (no packages) produces an empty report

## Dependencies
- Depends on: Task 1 — Add license policy configuration model and loader
