## Repository
trustify-backend

## Target Branch
main

## Description
Implement the service layer for generating license compliance reports (TC-9004). The service aggregates all packages associated with an SBOM — including transitive dependencies — by license type, then checks each license group against the configured policy to determine compliance status. The service must aggregate from existing package-license data without creating new database tables, and must meet p95 < 500ms for SBOMs with up to 1000 packages.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with generate_report method that aggregates packages by license and checks compliance

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — export license_report module and integrate with SbomService

## Implementation Notes
Follow the existing service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService). The service should:

1. Accept an SBOM ID and a LicensePolicy reference
2. Query the database for all packages linked to the SBOM via the sbom_package join table (entity/src/sbom_package.rs)
3. For each package, retrieve its license mappings from the package_license table (entity/src/package_license.rs)
4. Walk transitive dependencies through the sbom_package relationships to include all indirect dependencies
5. Group packages by license identifier
6. For each group, check the license against the LicensePolicy to determine compliance
7. Return a ComplianceReport

Per CONVENTIONS.md §Error handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping on fallible operations. See `common/src/error.rs` for the AppError enum.
Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` service file scope.

Per CONVENTIONS.md §Query helpers: use `common/src/db/query.rs` shared query builder helpers for filtering and pagination where applicable.
Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` service file scope.

Per CONVENTIONS.md §Module pattern: follow the model/ + service/ + endpoints/ structure. The service logic belongs in the service/ directory.
Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` module file scope.

For the performance requirement (p95 < 500ms for 1000 packages), consider batch-loading package-license relationships rather than N+1 queries. Use SeaORM's eager loading or a single join query to fetch all package-license pairs for the SBOM in one database round-trip.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service pattern for SBOM database queries; follow its constructor and method patterns
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/package_license.rs` — package-license entity for license aggregation queries
- `entity/src/sbom_package.rs` — SBOM-package join table entity for dependency traversal
- `common/src/error.rs::AppError` — standard error type for Result returns
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package service for reference on querying package data

## Acceptance Criteria
- [ ] Service generates a ComplianceReport for a given SBOM ID
- [ ] Report groups all packages by their license type (SPDX identifier)
- [ ] Each license group includes a `compliant` boolean flag based on the configured LicensePolicy
- [ ] Transitive dependencies are included in the report (full dependency tree walk)
- [ ] No new database tables are created — the service aggregates from existing package-license data
- [ ] Report generation completes within p95 < 500ms for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Unit test: report correctly groups packages by license when given a known set of packages
- [ ] Unit test: compliant flag is true for allowed licenses and false for denied licenses
- [ ] Unit test: transitive dependencies are included in license groups
- [ ] Unit test: returns an error (not a panic) when SBOM ID does not exist

## Dependencies
- Depends on: Task 1 — Add license policy configuration and compliance report models
