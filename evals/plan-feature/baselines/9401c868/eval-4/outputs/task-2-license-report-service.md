## Repository
trustify-backend

## Target Branch
main

## Description
Add the license compliance report service that generates a grouped license report for a given SBOM. The service fetches all packages associated with the SBOM (including transitive dependencies), groups them by license type using the package-license mapping, and checks each group against the configured license policy to determine compliance.

This is the core business logic for the license compliance report feature (TC-9004). The service is consumed by the endpoint handler (Task 3).

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` -- `LicenseReportService` with a `generate_report(sbom_id, db, policy)` method that: (1) queries all packages linked to the SBOM via `sbom_package` including transitive dependencies, (2) fetches license mappings from `package_license`, (3) groups packages by license, (4) checks each group against the `LicensePolicy` to set the `compliant` flag, (5) returns a `ComplianceReport`

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- Add `pub mod license_report;` to expose the new service module and integrate with `SbomService` if appropriate

## Implementation Notes
- Follow the service pattern established by `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`: the service methods accept a database connection and return `Result<T, AppError>`.
- To include transitive dependencies, walk the full dependency tree by joining `sbom_package` (which links SBOMs to packages) with `package_license` (which maps packages to licenses). The `sbom_package` join table connects the SBOM to its direct packages; transitive dependencies are packages linked through the dependency graph. Use SeaORM query builder patterns from `common/src/db/query.rs` for the joins.
- The compliance check logic: for each license group, set `compliant = true` if the license appears in `policy.allowed` or does not appear in `policy.denied`. If it appears in `policy.denied`, set `compliant = false`. If a license is in neither list, default to `compliant = true` (allowlist model) or apply configurable default behavior.
- Performance requirement: p95 < 500ms for SBOMs with up to 1000 packages. Use batch queries rather than N+1 patterns. Fetch all package-license mappings in a single query rather than per-package lookups.
- Per CONVENTIONS.md: services follow the `service/` directory structure within the domain module and use `Result<T, AppError>` with `.context()` error wrapping.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` module scope.
- Per CONVENTIONS.md: use SeaORM for database queries following the patterns in existing service files.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- Demonstrates the service pattern (method signatures, DB access, error handling) and contains `fetch` and `list` methods that show how to query SBOM-related data
- `common/src/db/query.rs` -- Shared query builder helpers for filtering, pagination, and sorting; use for constructing the package-license join query
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity; the primary table for finding packages belonging to an SBOM
- `entity/src/package_license.rs` -- Package-License mapping entity; used to look up the license for each package
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- Shows how to query package data; may contain reusable query patterns for package lookups

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report()` accepts an SBOM ID, database connection, and license policy
- [ ] Report correctly groups all packages by their license type
- [ ] Transitive dependency packages are included in the report (not just direct SBOM packages)
- [ ] Each license group has a `compliant` flag set based on the license policy
- [ ] Packages with licenses in the `denied` list are flagged as non-compliant
- [ ] Packages with licenses in the `allowed` list are flagged as compliant
- [ ] The service returns `AppError` for invalid SBOM IDs (SBOM not found)
- [ ] No N+1 query patterns -- package-license data is fetched in batch queries

## Test Requirements
- [ ] Unit test: service returns a report with packages grouped by license for a known SBOM
- [ ] Unit test: service correctly flags non-compliant licenses based on the denied list
- [ ] Unit test: service correctly flags compliant licenses based on the allowed list
- [ ] Unit test: transitive dependencies are included in the license groups
- [ ] Unit test: service returns an error when the SBOM ID does not exist
- [ ] Unit test: service handles packages with no license mapping gracefully (e.g., groups them under "Unknown")

## Dependencies
- Depends on: Task 1 -- Add license policy model and compliance report data structures
