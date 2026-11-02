## Repository
trustify-backend

## Target Branch
main

## Description
Create `LicenseReportService` that generates a license compliance report for a given SBOM. The service walks the SBOM's package tree (including transitive dependencies), groups packages by license, and checks each group's compliance against the configured `LicensePolicy`.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with a `generate_report(sbom_id, policy)` method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to export the new service module

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for database access patterns and error handling.
- Use SeaORM queries against `entity/src/sbom_package.rs` (SBOM-Package join table) and `entity/src/package_license.rs` (Package-License mapping) to retrieve packages and their licenses for a given SBOM.
- For transitive dependency walking: query `sbom_package` for all packages linked to the SBOM ID, then join with `package_license` to get license data. The SBOM-Package relationship already includes transitive dependencies from ingestion.
- Use `common/src/db/query.rs` for query builder helpers if pagination or filtering is needed.
- Wrap errors with `.context()` per the error handling convention in `common/src/error.rs` (AppError).
- The compliance check: for each license group, check if the license SPDX identifier appears in `LicensePolicy.denied_licenses` (non-compliant) or `LicensePolicy.review_required_licenses` (flagged). Licenses in `allowed_licenses` or not in any list are compliant.
- Per CONVENTIONS.md §Module pattern: service module follows the established `model/ + service/ + endpoints/` structure. Applies: task modifies `modules/fundamental/src/sbom/service/mod.rs` matching the convention's module structure scope.
- Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/mod.rs` matching the convention's Rust service scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service for SBOM operations, shows database query patterns and error handling
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package service with fetch/list methods that access the same entity tables
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report` accepts an SBOM ID and LicensePolicy, returns `Result<LicenseReport, AppError>`
- [ ] All packages in the SBOM (including transitive dependencies) are included in the report
- [ ] Packages are grouped by license type
- [ ] Each group's `compliant` flag is correctly set based on the LicensePolicy
- [ ] Returns an appropriate error when the SBOM ID does not exist

## Test Requirements
- [ ] Unit test: generate report for an SBOM with multiple license types, verify grouping
- [ ] Unit test: generate report with a denied license, verify `compliant: false` on that group
- [ ] Unit test: generate report for a non-existent SBOM, verify error response
- [ ] Unit test: verify transitive dependencies are included in the report

## Dependencies
- Depends on: Task 1 — License policy model
- Depends on: Task 2 — License report model
