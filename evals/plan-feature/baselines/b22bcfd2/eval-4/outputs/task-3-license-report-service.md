## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `LicenseReportService` that aggregates package-license data from existing database entities, walks transitive dependencies, and evaluates compliance against the configured license policy. This is the core business logic for the license compliance report feature.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with method `async fn generate_report(&self, sbom_id: Uuid, db: &DbConn, policy: &LicensePolicy) -> Result<LicenseReport, AppError>` that queries packages for the given SBOM, groups them by license, walks transitive dependencies via `sbom_package` relationships, and flags non-compliant groups

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module

## Implementation Notes
Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`). Use SeaORM queries against the `entity/src/sbom_package.rs` join table to get all packages for an SBOM, then join with `entity/src/package_license.rs` to get license data. For transitive dependency walking, query the `sbom_package` relationship table recursively. Use `common/src/db/query.rs` helpers for query construction. Group results by license string using a `HashMap<String, Vec<PackageLicenseInfo>>`, then evaluate each group against the `LicensePolicy::check_license()` method. Return `Result<LicenseReport, AppError>` using the error pattern from `common/src/error.rs` with `.context()` wrapping on database errors.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Pattern for database query structure and error handling
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Reuse package fetching logic
- `common/src/db/query.rs` — Query builder helpers for filtering and joining
- `common/src/error.rs::AppError` — Error handling pattern

## Acceptance Criteria
- [ ] Service queries all packages for a given SBOM ID including transitive dependencies
- [ ] Packages are grouped by license identifier
- [ ] Each group's compliance is evaluated against the provided LicensePolicy
- [ ] Service returns an error if the SBOM ID does not exist
- [ ] Report includes a summary with total, compliant, and non-compliant counts
- [ ] Performance: handles SBOMs with up to 1000 packages within acceptable query time

## Test Requirements
- [ ] Integration test: generate report for an SBOM with packages having mixed licenses
- [ ] Integration test: verify transitive dependencies are included in the report
- [ ] Integration test: verify non-existent SBOM ID returns appropriate error
- [ ] Unit test: grouping logic correctly groups packages by license

## Dependencies
- Depends on: Task 1 — License policy configuration (uses LicensePolicy)
- Depends on: Task 2 — License report model (uses LicenseReport, LicenseGroup structs)
