# Task 3 -- Add license report service

**Summary:** Add LicenseReportService to aggregate license data and evaluate compliance

**Priority:** Major
**Fix Versions:** RHTPA 1.5.0
**Labels:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `LicenseReportService` that aggregates package-license data from existing database tables for a given SBOM, walks transitive dependencies, groups packages by license, and evaluates compliance against the license policy. This is the core business logic for the license compliance report feature.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` -- `LicenseReportService` with methods to generate the compliance report

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- add `pub mod license_report` to expose the new service module

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/` -- see `sbom.rs` (`SbomService`) for the query pattern, database access, and error handling approach
- The service should:
  1. Accept an SBOM ID and a reference to `LicensePolicy` (from Task 1)
  2. Query the `sbom_package` join table to get all packages for the SBOM
  3. For each package, query the `package_license` table to get license mappings
  4. Walk transitive dependencies: use the `sbom_package` relationships to traverse the full dependency tree, collecting licenses from all transitive dependencies (not just direct)
  5. Group packages by license identifier
  6. For each group, evaluate compliance using `LicensePolicy::is_compliant()`
  7. Return a `LicenseReport` struct (from Task 2)
- Use `common/src/db/query.rs` query helpers for database access where applicable
- Performance requirement: p95 < 500ms for SBOMs with up to 1000 packages. Consider:
  - Batch loading package-license mappings instead of N+1 queries
  - Using a single query with JOINs across `sbom_package` and `package_license` tables
  - Collecting all data in memory for grouping (acceptable for up to 1000 packages)
- No new database tables -- aggregate exclusively from existing `package`, `sbom_package`, and `package_license` entities
- Per CONVENTIONS.md (Key Conventions -- Error handling): all service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` module scope.
- Per CONVENTIONS.md (Key Conventions -- Query helpers): use shared filtering and query helpers from `common/src/db/query.rs`. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- reference for service structure, database access patterns, and error handling
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- reference for querying package data
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination
- `entity/src/package_license.rs` -- Package-License mapping entity definition
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity definition

## Acceptance Criteria
- [ ] Service generates a complete license report for a given SBOM ID
- [ ] All transitive dependency licenses are included (not just direct dependencies)
- [ ] Packages are correctly grouped by license identifier
- [ ] Compliance flags correctly reflect the license policy evaluation
- [ ] Report counts (total_packages, compliant_count, non_compliant_count) are accurate
- [ ] Performance: handles SBOMs with 1000 packages within acceptable response time

## Test Requirements
- [ ] Unit test: report correctly groups packages by license
- [ ] Unit test: transitive dependencies are included in the report
- [ ] Unit test: compliance flags match policy evaluation for allowed licenses
- [ ] Unit test: compliance flags match policy evaluation for denied licenses
- [ ] Unit test: report with no packages returns empty groups
- [ ] Unit test: report counts are accurate

## Dependencies
- Depends on: Task 1 -- Add license policy configuration model
- Depends on: Task 2 -- Add license compliance report model structs
