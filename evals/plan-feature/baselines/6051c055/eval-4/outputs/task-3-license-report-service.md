## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `LicenseReportService` that generates a license compliance report for a given SBOM. The service queries all packages associated with an SBOM (via the `sbom_package` join table), retrieves their license information (via `package_license`), groups packages by license, classifies each group against the license policy, and detects conflicting licenses on individual packages.

## Files to Modify
- `modules/fundamental/src/license_report/mod.rs` — add `pub mod service;` to expose the service submodule

## Files to Create
- `modules/fundamental/src/license_report/service.rs` — `LicenseReportService` with method `generate_report(db: &DatabaseConnection, sbom_id: Uuid) -> Result<LicenseReport, AppError>`

## Implementation Notes
- Follow the service pattern from `modules/fundamental/src/package/service/mod.rs` and `modules/fundamental/src/sbom/service/sbom.rs`
- Query flow:
  1. Verify SBOM exists using `SbomService` — return 404 `AppError` if not found
  2. Query `sbom_package` join table to get all package IDs for the SBOM
  3. For each package, query `package_license` to get associated licenses
  4. Load all `LicensePolicy` entries to build a classification lookup map (license_spdx -> Classification)
  5. Group packages by license SPDX expression
  6. For each group, look up classification from policy; default to `ReviewRequired` if no policy entry exists
  7. Detect conflicts: any package with multiple licenses where at least one is `Denied` or classifications differ (e.g., copyleft + permissive)
  8. Compute summary statistics (total, compliant, non-compliant, review-required counts)
  9. Assemble and return `LicenseReport`
- Use SeaORM query builder for database access, not raw SQL
- Handle the case where an SBOM has no packages (return empty report, not an error)
- Use `common/src/error.rs` `AppError` for error handling

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report` returns a valid `LicenseReport` for a given SBOM ID
- [ ] Packages are correctly grouped by license SPDX identifier
- [ ] Each group has the correct classification from the license policy table
- [ ] Packages with no matching policy default to `ReviewRequired`
- [ ] Packages with multiple conflicting licenses appear in the `conflicts` list
- [ ] Summary statistics are accurate (total_packages, compliant_count, etc.)
- [ ] Returns 404 error for non-existent SBOM IDs
- [ ] Returns empty report (not error) for SBOMs with no packages

## Test Requirements
- [ ] Unit test: report generation with single-license packages, all classified
- [ ] Unit test: report generation with a package having conflicting licenses
- [ ] Unit test: packages with no policy entry default to ReviewRequired
- [ ] Unit test: empty SBOM returns empty report
- [ ] Unit test: non-existent SBOM returns appropriate error
