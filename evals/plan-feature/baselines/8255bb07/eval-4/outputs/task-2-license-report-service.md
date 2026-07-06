## Repository
trustify-backend

## Target Branch
main

## Description
Add a LicenseReportService that generates a license compliance report for a given SBOM. The service fetches all packages associated with the SBOM (including transitive dependencies by walking the full dependency tree), groups them by license type, and flags each group as compliant or non-compliant based on the configured license policy. The service must meet the p95 < 500ms performance target for SBOMs with up to 1000 packages.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- add `pub mod license_report;` to export the new service module
- `modules/fundamental/src/sbom/mod.rs` -- re-export the license report service if needed for external access

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` -- LicenseReportService with a `generate_report(db: &DbConn, sbom_id: Uuid, policy: &LicensePolicy) -> Result<LicenseReport, AppError>` method that: (1) queries all packages for the SBOM via the sbom_package join table, (2) walks transitive dependencies using the package relationship graph, (3) fetches license data from the package_license mapping, (4) groups packages by license string, (5) checks each group against the policy's allowed/denied lists, (6) returns the LicenseReport with compliant flags

## Implementation Notes
- Per Key Conventions "Module pattern": follow the established service module pattern. Place the service at `modules/fundamental/src/sbom/service/license_report.rs` alongside existing `sbom.rs`.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's module service file scope.
- Per Key Conventions "Error handling": all service methods return `Result<T, AppError>` with `.context()` wrapping on database query errors.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust source file scope.
- Per Key Conventions "Query helpers": use shared query builder helpers from `common/src/db/query.rs` for filtering and joining package data efficiently.
  Applies: task modifies `modules/fundamental/src/sbom/service/mod.rs` matching the convention's Rust source file scope.
- No new database tables are required (per NFR). Aggregate from existing `sbom_package`, `package`, and `package_license` entities.
- For transitive dependency traversal, use a BFS/DFS approach over the package relationship graph. Consider batch-loading packages to avoid N+1 queries and meet the p95 < 500ms performance requirement.
- License comparison should be case-insensitive and handle SPDX license identifiers (e.g., "MIT", "Apache-2.0").

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- existing SBOM service with fetch and list methods; reference its database access patterns for connection handling and error wrapping
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- existing package service; reference its query patterns for fetching package data
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity; use for querying packages belonging to an SBOM
- `entity/src/package_license.rs` -- Package-License mapping entity; use for fetching license data per package
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting; reuse for efficient package queries

## Acceptance Criteria
- [ ] LicenseReportService.generate_report returns a LicenseReport with packages grouped by license
- [ ] Each LicenseGroup has a `compliant` flag set to `false` when the license appears in the policy's denied list, `true` when in the allowed list or not in the denied list
- [ ] Transitive dependencies are included in the report (packages reachable through the full dependency tree, not just direct dependencies)
- [ ] Report generation completes within 500ms (p95) for SBOMs with up to 1000 packages
- [ ] Service returns AppError with descriptive context when the SBOM ID does not exist

## Test Requirements
- [ ] Unit test: service correctly groups packages by license type
- [ ] Unit test: service flags denied licenses as non-compliant
- [ ] Unit test: service marks allowed licenses as compliant
- [ ] Unit test: service includes transitive dependencies in the report
- [ ] Unit test: service returns an error for a non-existent SBOM ID
- [ ] Unit test: service handles packages with no license data (groups them under an "Unknown" license)

## Dependencies
- Depends on: Task 1 -- Add license policy configuration and compliance report model
