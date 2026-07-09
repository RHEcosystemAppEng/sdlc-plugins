## Repository
trustify-backend

## Target Branch
main

## Description
Add the license report response model and service layer that aggregates package-license data from existing database tables for a given SBOM. The service queries the `package_license` and `sbom_package` entities to collect all packages (including transitive dependencies) associated with an SBOM, groups them by license type, and checks each group's compliance against the configurable license policy from Task 1.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Define `LicenseReportGroup` (license name, list of packages, compliant flag) and `LicenseReport` (list of groups, overall compliance summary) response structs
- `modules/fundamental/src/sbom/service/license_report.rs` — Implement `LicenseReportService` with a method to generate the report for a given SBOM ID: query packages via `sbom_package` join, fetch licenses via `package_license`, group by license, apply policy compliance check

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to re-export the new model
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to re-export the new service
- `modules/fundamental/src/sbom/mod.rs` — Ensure new model and service modules are accessible

## API Changes
- No HTTP-level API changes in this task (endpoint is added in Task 3)

## Implementation Notes
- The `LicenseReportGroup` struct should include: `license: String` (SPDX identifier), `packages: Vec<PackageSummary>` (reuse existing `PackageSummary` from `package/model/summary.rs`), `compliant: bool` (determined by the license policy)
- The `LicenseReport` struct should include: `groups: Vec<LicenseReportGroup>`, `total_packages: usize`, `compliant_count: usize`, `non_compliant_count: usize`
- Transitive dependency walking: query all `sbom_package` records for the given SBOM ID, then join with `package_license` to get the license for each package. The `sbom_package` table already captures the full dependency tree as stored during ingestion
- Use SeaORM query builder patterns consistent with existing service implementations (e.g., `SbomService` in `service/sbom.rs`)
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use a single query with joins rather than N+1 queries. Consider using `find_with_related()` or a raw SQL query if the ORM abstraction causes performance issues
- Per CONVENTIONS.md Key Conventions (Module Pattern): follow the established `model/ + service/ + endpoints/` structure.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md Key Conventions (Error Handling): all service methods must return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md Key Conventions (Framework): use SeaORM for all database queries. Follow the `SbomService` pattern for query construction.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust source file scope.
- No new database tables — aggregate from existing `package_license` and `sbom_package` entity data (per the feature's non-functional requirement)

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service pattern for SBOM queries; follow its structure for database access and error handling
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reuse this struct for the package entries within each license group rather than defining a new package type
- `entity/src/package_license.rs` — existing SeaORM entity for the package-license mapping; use this for the license query
- `entity/src/sbom_package.rs` — existing SeaORM entity for the SBOM-package join; use this to find all packages in an SBOM
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report(sbom_id)` returns a `LicenseReport` with packages grouped by license
- [ ] Each group's `compliant` flag reflects the license policy evaluation
- [ ] Transitive dependencies are included in the report (all packages linked via `sbom_package`)
- [ ] Report includes overall compliance summary counts
- [ ] No new database tables are created

## Test Requirements
- [ ] Unit test: generate report for an SBOM with packages having different licenses and verify grouping
- [ ] Unit test: verify compliance flags are correctly set based on a test license policy (allowed, denied, review_required)
- [ ] Unit test: verify transitive dependencies are included in the report
- [ ] Unit test: verify report for an SBOM with no packages returns an empty groups list

## Verification Commands
- `cargo test --package fundamental` — all unit tests pass
- `cargo build --package fundamental` — compiles without errors

## Dependencies
- Depends on: Task 1 — Add license policy configuration model
