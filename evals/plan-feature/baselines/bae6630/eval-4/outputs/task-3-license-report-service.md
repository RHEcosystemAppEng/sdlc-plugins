## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service that queries the database for all packages associated with an SBOM, groups them by license type, evaluates each group against the license policy, and returns a populated `LicenseReport` struct. This includes walking transitive dependencies via the SBOM-package relationship tables.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with a method `generate_report(sbom_id: Id, policy: &LicensePolicy) -> Result<LicenseReport, AppError>` that queries package-license data, groups by license, and flags compliance

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` and integrate `LicenseReportService` into the module

## Implementation Notes
- Query the `sbom_package` join table (`entity/src/sbom_package.rs`) to get all packages for the given SBOM ID, including transitive dependencies
- Join with `package_license` (`entity/src/package_license.rs`) to retrieve the license for each package
- Use the `package` entity (`entity/src/package.rs`) for package name and version information
- Group results by license string, creating a `LicenseGroup` for each unique license
- For each group, call `LicensePolicy::is_compliant()` to set the `compliant` flag
- Follow the query pattern from `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for database access patterns
- Use query helpers from `common/src/db/query.rs` for any filtering or pagination if needed
- Return errors wrapped with `.context()` to produce meaningful `AppError` messages, following the pattern in `common/src/error.rs`
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages; consider a single SQL query with GROUP BY rather than N+1 queries

## Acceptance Criteria
- [ ] Service correctly queries all packages (including transitive dependencies) for a given SBOM ID
- [ ] Packages are grouped by license type
- [ ] Each group has a correct `compliant` flag based on the license policy
- [ ] `total_packages` and `non_compliant_count` fields are accurately computed
- [ ] Non-existent SBOM IDs return an appropriate 404 error
- [ ] Performance is acceptable for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Unit tests with mock data verify correct grouping of packages by license
- [ ] Unit tests verify compliance flag is set correctly per policy
- [ ] Unit tests verify error handling for missing SBOM IDs
- [ ] Unit tests verify transitive dependencies are included

## Dependencies
- Depends on: Task 1 — Define license report model structs
- Depends on: Task 2 — Implement license policy configuration

## Digest
[sdlc-workflow] Description digest: sha256-md:a52c484527a1f10f67e993032ab2205a2634ec11022750ce84c1f4ef3c3fb96d
