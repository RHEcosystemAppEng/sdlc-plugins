# Task 3 — Add license report service with transitive dependency walking

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the core license report generation service that aggregates license data from existing package-license mappings, walks the full transitive dependency tree, groups packages by license, and checks each group against the configured license policy. This service is the core business logic for the license compliance feature.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with report generation logic

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) — accept a database connection/pool parameter and return `Result<T, AppError>`.
- The service function should:
  1. Fetch all packages associated with the given SBOM ID using the `sbom_package` join table entity (`entity/src/sbom_package.rs`)
  2. For each package, fetch license data from the `package_license` entity (`entity/src/package_license.rs`)
  3. Walk transitive dependencies: query `sbom_package` relationships recursively to find indirect dependencies, marking each as `transitive: true` in the report
  4. Group all packages (direct and transitive) by their license identifier
  5. For each license group, check the license against the `LicensePolicy` (from Task 1) and set the `compliant` flag and `policy_status` accordingly
  6. Assemble and return a `LicenseReport` (from Task 2)
- Use SeaORM query patterns consistent with existing services. Reference the query builder helpers in `common/src/db/query.rs` for any filtering or joining.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Consider:
  - Fetching all package-license data in a single query with joins rather than N+1 queries
  - Using `HashMap<String, Vec<PackageLicenseEntry>>` for efficient grouping
- No new database tables are required — aggregate from existing `package_license` and `sbom_package` data.
- Error handling: wrap all database operations with `.context()` per `common/src/error.rs::AppError` pattern.
- Per `docs/constraints.md` section 5.4: do not duplicate existing functionality — reuse PackageService query patterns where applicable.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Follow the same service method signature pattern (db pool parameter, Result return type)
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Existing package query logic; reuse query patterns for fetching package data
- `common/src/db/query.rs` — Shared query builder helpers for filtering and joining
- `entity/src/package_license.rs` — Package-License mapping entity for license data access
- `entity/src/sbom_package.rs` — SBOM-Package join table for dependency relationships

## Acceptance Criteria
- [ ] Service generates a complete license report for a given SBOM ID
- [ ] Transitive dependencies are included and correctly marked as transitive
- [ ] Packages are grouped by license identifier
- [ ] Each license group has correct compliance flags based on the configured policy
- [ ] Report counts (total_packages, compliant_count, non_compliant_count) are accurate

## Test Requirements
- [ ] Unit test: generate report for SBOM with packages under allowed licenses — all groups marked compliant
- [ ] Unit test: generate report for SBOM with a package under a denied license — that group marked non-compliant
- [ ] Unit test: generate report for SBOM with transitive dependencies — transitive packages included and flagged
- [ ] Unit test: generate report for SBOM with no packages — returns empty report with zero counts
- [ ] Unit test: verify package deduplication — a package appearing multiple times in the dependency tree appears once in the report

## Verification Commands
- `cargo build -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental` — all tests pass

## Dependencies
- Depends on: Task 1 — Add license policy configuration model and loader
- Depends on: Task 2 — Add license compliance report model
