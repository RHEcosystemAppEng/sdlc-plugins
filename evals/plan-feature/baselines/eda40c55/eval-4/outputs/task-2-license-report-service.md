## Repository
trustify-backend

## Target Branch
main

## Description
Add the license report model and service logic that generates a structured compliance report for a given SBOM. The service queries all packages associated with the SBOM (including transitive dependencies), groups them by license type, and checks each group against the configured license policy to produce compliance flags. The report must meet the p95 < 500ms performance target for SBOMs with up to 1000 packages.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReport and LicenseReportGroup structs representing the grouped compliance report response
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with the `generate_report` method that queries packages, walks transitive dependencies, groups by license, and checks compliance

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod license_report;` to expose the report model
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod license_report;` to expose the report service

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW (model only; endpoint wiring is Task 3): returns `LicenseReport { groups: Vec<LicenseReportGroup> }` where each group contains `{ license: String, packages: Vec<PackageLicenseEntry>, compliant: bool }`

## Implementation Notes
- Define response structs:
  - `LicenseReportGroup { license: String, packages: Vec<PackageLicenseEntry>, compliant: bool }`
  - `LicenseReport { groups: Vec<LicenseReportGroup> }`
  - `PackageLicenseEntry { name: String, version: String, purl: Option<String> }`
- Implement `LicenseReportService::generate_report(db: &DbConn, sbom_id: Uuid, policy: &LicensePolicy) -> Result<LicenseReport, AppError>`:
  1. Query `sbom_package` join table to get all packages for the SBOM
  2. For each package, query `package_license` to get license identifiers
  3. Walk the full dependency tree by following `sbom_package` relationships for transitive dependencies
  4. Group packages by their license SPDX identifier
  5. For each group, call `policy.is_compliant(license)` to set the `compliant` flag
- Use SeaORM query patterns from `modules/fundamental/src/sbom/service/sbom.rs` as the reference implementation for database queries
- Use `common/src/db/query.rs` helpers for query building
- No new database tables — aggregate from existing `package_license` and `sbom_package` entities per the NFRs
- Performance: use batch queries rather than N+1 patterns to meet the p95 < 500ms target for SBOMs with up to 1000 packages
- Per CONVENTIONS.md: follow the module pattern (model/ + service/ + endpoints/) — this task adds the model and service layers.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` module scope.
- Per CONVENTIONS.md: all service methods return `Result<T, AppError>` with `.context()` error wrapping.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` error handling scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference for SeaORM query patterns, database connection handling, and error wrapping
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages belonging to an SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for retrieving license data per package
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing package model with license field; reference for field naming conventions

## Acceptance Criteria
- [ ] `LicenseReport` and `LicenseReportGroup` structs are defined with correct serialization
- [ ] `generate_report` queries all packages (including transitive dependencies) for a given SBOM
- [ ] Packages are correctly grouped by license type
- [ ] Each group's `compliant` flag reflects the license policy check
- [ ] Packages with no license data are handled gracefully (grouped under "Unknown" or similar)
- [ ] Report generation completes within 500ms for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Unit test: generate report for an SBOM with packages under a single compliant license
- [ ] Unit test: generate report for an SBOM with mixed compliant and non-compliant licenses
- [ ] Unit test: verify transitive dependencies are included in the report
- [ ] Unit test: verify packages with no license data are grouped correctly
- [ ] Unit test: verify performance — report generation for 1000 packages completes within budget

## Dependencies
- Depends on: Task 1 — Add license policy configuration model
