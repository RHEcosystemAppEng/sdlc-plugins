## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service that aggregates package-license data for an SBOM, walks the transitive dependency tree, evaluates compliance against the configured license policy, and returns a `LicenseReport` grouped by license type. This service must meet the p95 < 500ms performance target for SBOMs with up to 1000 packages. No new database tables are created — the service aggregates from existing `package_license`, `sbom_package`, and `package` entities.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` (or method on existing `SbomService`) that queries package-license data, resolves transitive dependencies, groups by license, and evaluates compliance

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` or extend `SbomService` with the report method

## API Changes
- Internal service API: `generate_license_report(sbom_id: Id) -> Result<LicenseReport, AppError>` — NEW: aggregates package licenses for the given SBOM, walks transitive dependencies, and returns grouped/compliance-evaluated results

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` for database access patterns and error handling.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust module file scope.
- Per Key Conventions (Error handling): all service methods return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust source file scope.
- Per Key Conventions (Query helpers): use shared filtering and query builder helpers from `common/src/db/query.rs` for database queries.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust source file scope.
- Query the `sbom_package` join table to get all packages for the SBOM, then join with `package_license` to get license mappings. Use `entity/src/sbom_package.rs` and `entity/src/package_license.rs` entities.
- For transitive dependency resolution: walk the dependency graph starting from direct SBOM packages through their dependency relationships. The `sbom_package` entity likely captures the full dependency tree from SBOM ingestion.
- Group packages by their license identifier, instantiate `LicenseReportGroup` for each group, and evaluate compliance using `LicensePolicy::is_compliant()` from the common crate.
- Performance: use a single query with JOINs rather than N+1 queries. Consider batch loading all package-license mappings for the SBOM in one query, then performing in-memory grouping. Target p95 < 500ms for 1000 packages.
- No new database tables — aggregate from existing `package_license`, `sbom_package`, and `package` entities only.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference for service structure and database access pattern
- `modules/fundamental/src/package/service/mod.rs::PackageService` — reference for querying package data
- `common/src/db/query.rs` — shared query builder helpers for filtering and joins
- `common/src/license_policy.rs::LicensePolicy` — the policy evaluator created in Task 2
- `entity/src/package_license.rs` — Package-License mapping entity for querying license data
- `entity/src/sbom_package.rs` — SBOM-Package join table for resolving package membership

## Acceptance Criteria
- [ ] Service method returns a `LicenseReport` with packages grouped by license
- [ ] Transitive dependencies are included in the report (not just direct packages)
- [ ] Each `LicenseReportGroup` has its `compliant` flag set based on the configured license policy
- [ ] Packages with no license mapping are handled gracefully (e.g., grouped under "Unknown" or similar)
- [ ] Querying a non-existent SBOM ID returns an appropriate error
- [ ] No new database tables are created — only existing entities are queried

## Test Requirements
- [ ] Unit test: service correctly groups packages by license
- [ ] Unit test: transitive dependencies are included in the grouping
- [ ] Unit test: compliance flags are set correctly based on the license policy
- [ ] Unit test: packages without license data are handled without panicking
- [ ] Unit test: non-existent SBOM ID returns an error
- [ ] Performance: verify report generation completes within 500ms for a test dataset of 1000 packages

## Dependencies
- Depends on: Task 1 — Add license compliance report response types
- Depends on: Task 2 — Add license policy configuration
