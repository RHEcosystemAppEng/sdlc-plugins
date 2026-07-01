## Repository
trustify-backend

## Target Branch
main

## Description
Add a license report service that generates a compliance report for a given SBOM. The service queries all packages associated with the SBOM (including transitive dependencies), groups them by license type, and evaluates each group against the configured license policy to produce compliance flags.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- add module declaration for the new license report service file

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` -- implement `LicenseReportService` with a `generate_report(sbom_id, policy)` method that queries package-license data, walks transitive dependencies, groups by license, and flags non-compliant licenses

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) -- services take a database connection/pool parameter and return `Result<T, AppError>`.
- Use the error handling pattern from `common/src/error.rs` -- return `Result<T, AppError>` and use `.context()` wrapping for all database operations.
- Query the `sbom_package` join table (`entity/src/sbom_package.rs`) to get all packages for the SBOM, then join with `package_license` (`entity/src/package_license.rs`) to get license data.
- For transitive dependency walking: follow the SBOM package relationships in the `sbom_package` entity to traverse the full dependency tree. If no explicit dependency graph exists, treat all packages linked to the SBOM as direct or transitive (flattened view).
- Group packages by their license SPDX identifier, then check each license against the `LicensePolicy` to set the `compliant` flag.
- Use shared query builder helpers from `common/src/db/query.rs` for any filtering or pagination needs.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Consider batch-loading packages rather than N+1 queries.
- Per CONVENTIONS.md (Key Conventions): all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` service file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- existing service pattern for SBOM operations; follow the same constructor, connection handling, and error patterns
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- package query patterns that can inform the license data fetching logic
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` -- error enum with `IntoResponse` implementation

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report` returns a `LicenseReport` with packages grouped by license
- [ ] Transitive dependency licenses are included in the report
- [ ] Each license group has a correct `compliant` flag based on the provided policy
- [ ] Non-compliant licenses are flagged when they appear on the policy deny list
- [ ] Service handles the case of an SBOM with no packages gracefully (returns empty groups)

## Test Requirements
- [ ] Unit test for grouping packages by license type
- [ ] Unit test for compliance flag logic with allowlist policy
- [ ] Unit test for compliance flag logic with denylist policy
- [ ] Unit test for handling an SBOM with no associated packages
- [ ] Unit test for handling packages with no license data

## Dependencies
- Depends on: Task 1 -- Add license compliance report model types

## Description Digest
sha256-md:51ef64ee745f9e10f91812bfe61c50c3653814bea2321a333dacbd13bc762fd1
