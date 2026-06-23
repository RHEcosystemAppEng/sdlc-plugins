# Task 3 — Add license compliance report service

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the service layer that generates a license compliance report for a given SBOM. The service aggregates package-license data from existing database tables, walks the full dependency tree to include transitive dependencies, groups packages by license type, and applies the license policy to flag non-compliant groups. This service is consumed by the endpoint added in Task 4.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with the `generate_report` method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — re-export `license_report` module

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (the `SbomService` struct) — the new `LicenseReportService` should accept a database connection and the `LicensePolicy` (from Task 2) as dependencies.
- The core method `generate_report(sbom_id: Uuid) -> Result<LicenseReport, AppError>` should:
  1. Query the `sbom_package` join table (entity defined in `entity/src/sbom_package.rs`) to get all packages in the SBOM.
  2. For each package, look up license data via the `package_license` mapping (entity in `entity/src/package_license.rs`).
  3. Walk transitive dependencies: follow the package dependency graph through `sbom_package` relationships to include licenses from all transitive dependencies, not just direct ones.
  4. Group packages by their license identifier.
  5. For each group, evaluate `LicensePolicy::is_compliant()` to set the `compliant` flag.
  6. Return a `LicenseReport` struct (from Task 1) with the populated groups.
- Use the query helpers from `common/src/db/query.rs` for any database queries that need filtering or sorting.
- Performance requirement: p95 < 500ms for SBOMs with up to 1000 packages. Use batch queries rather than N+1 queries — fetch all `sbom_package` and `package_license` records for the SBOM in bulk, then assemble the grouping in memory.
- No new database tables are needed — aggregate from existing `package`, `sbom_package`, and `package_license` entities.
- Error handling: all fallible operations should use `.context()` wrapping and return `AppError`, consistent with `common/src/error.rs`.
- Per docs/constraints.md section 5 (Code Change Rules): inspect code before modifying; reuse existing utilities; follow referenced patterns.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — follow the same service struct pattern (constructor, db connection injection)
- `modules/fundamental/src/package/service/mod.rs::PackageService` — may contain query patterns for fetching packages that can be reused or extended
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/package_license.rs` — the SeaORM entity for package-to-license mapping, the primary data source for license information
- `entity/src/sbom_package.rs` — the SeaORM entity for SBOM-to-package relationships, needed for dependency traversal

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report()` returns a `LicenseReport` with packages correctly grouped by license
- [ ] Transitive dependency licenses are included in the report (not just direct dependencies)
- [ ] Each license group has the correct `compliant` flag based on the configured policy
- [ ] No new database tables are created — only existing entities are queried
- [ ] Performance: report generation completes within 500ms for an SBOM with 1000 packages (measured in integration tests)

## Test Requirements
- [ ] Unit test: given a mock set of packages with known licenses, `generate_report` produces correct groupings
- [ ] Unit test: transitive dependencies are included in the license groups
- [ ] Unit test: compliance flags reflect the license policy (allowed license -> compliant=true, denied license -> compliant=false)
- [ ] Unit test: SBOM with no packages returns an empty report (no groups)
- [ ] Unit test: packages with unknown/missing licenses are handled gracefully (grouped under an "Unknown" or null license group)

## Dependencies
- Depends on: Task 1 — Add license compliance report model types
- Depends on: Task 2 — Add configurable license policy support

sha256-md:2720521be3a02ea90aa3c969579ef1dd75f8a94fa23da74bde47f7e813999abe
