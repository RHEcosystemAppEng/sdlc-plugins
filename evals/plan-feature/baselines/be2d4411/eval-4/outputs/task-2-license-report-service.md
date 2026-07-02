## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license compliance report service that aggregates package-license data for a given SBOM, walks transitive dependencies to include the full dependency tree, groups packages by license type, and checks each group against the license policy to determine compliance. This service must meet the p95 < 500ms performance target for SBOMs with up to 1000 packages.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — re-export the new license_report service module

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with a `generate_report` method that takes an SBOM ID and returns a LicenseReport

## Implementation Notes
- Follow the service module pattern established in `modules/fundamental/src/sbom/service/sbom.rs` — the `SbomService` struct demonstrates the conventional approach for database-backed services (dependency injection of the database connection pool, async methods returning `Result<T, AppError>`).
- Use `common/src/db/query.rs` for shared query builder helpers if filtering or sorting is needed when querying package-license data.
- The service must aggregate data from existing tables — no new database tables are permitted (per NFR). The key entity relationships are:
  - `entity/src/sbom_package.rs` — SBOM-to-Package join table (identifies which packages belong to an SBOM)
  - `entity/src/package_license.rs` — Package-to-License mapping (identifies each package's license)
  - `entity/src/package.rs` — Package entity
- For transitive dependency resolution: query the `sbom_package` join table to get all packages (direct and transitive) associated with the SBOM ID. The existing ingestion pipeline in `modules/ingestor/src/graph/sbom/mod.rs` already resolves and stores transitive dependencies during SBOM ingestion, so the full dependency tree is available in `sbom_package`.
- Group the resulting packages by their license identifier from `package_license`, construct `LicenseGroup` instances, and check compliance using `LicensePolicy::is_compliant` from Task 1.
- Error handling: wrap all database operations with `.context()` per the `AppError` pattern in `common/src/error.rs`. Return `AppError::NotFound` when the SBOM ID does not exist.
- Performance: use a single query with JOINs across sbom_package, package, and package_license rather than N+1 queries. Consider using `HashMap<String, Vec<PackageSummary>>` for in-memory grouping to achieve O(n) grouping.
- Per docs/constraints.md section 5: error handling must use `Result<T, AppError>` with `.context()` wrapping.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference implementation for service struct pattern, DB connection injection, async methods
- `modules/fundamental/src/package/service/mod.rs::PackageService` — reference for querying package data from the database
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/sbom_package.rs` — join table entity for SBOM-package relationships
- `entity/src/package_license.rs` — entity for package-license mappings
- `common/src/error.rs::AppError` — error handling enum

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report` returns a `LicenseReport` with packages grouped by license
- [ ] Transitive dependencies are included in the report (all packages from sbom_package join table)
- [ ] Each license group has a correct `compliant` flag based on the configured policy
- [ ] Report summary contains accurate total_packages, compliant_count, and non_compliant_count
- [ ] Returns `AppError::NotFound` for non-existent SBOM IDs
- [ ] Single-query approach (no N+1) for SBOM-package-license data retrieval

## Test Requirements
- [ ] Unit/integration test: generate report for SBOM with all compliant licenses
- [ ] Unit/integration test: generate report for SBOM with mixed compliant and non-compliant licenses
- [ ] Unit/integration test: generate report for SBOM with transitive dependencies included
- [ ] Unit/integration test: generate report for non-existent SBOM returns NotFound error
- [ ] Unit/integration test: generate report for SBOM with no packages returns empty groups

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental -- license_report` — all service tests pass

## Dependencies
- Depends on: Task 1 — Add license report model types (LicenseReport, LicenseGroup, LicensePolicy structs)

[sdlc-workflow] Description digest: sha256-md:ef0171f94383ba014ea7bd263d37fb955a6e2ab488f6a2b2c5a63577ebdd8f49
