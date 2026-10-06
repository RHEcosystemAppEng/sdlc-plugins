## Repository
trustify-backend

## Target Branch
main

## Description
Add the license compliance report service that aggregates package license data from existing database tables, walks the transitive dependency tree, and applies the configurable compliance policy to produce a grouped license report. This service uses the existing `package_license` and `sbom_package` entities — no new database tables are needed.

The service must meet the performance target of p95 < 500ms for SBOMs with up to 1000 packages.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — export the new `license_report` service module
- `modules/fundamental/src/sbom/model/license_report.rs` — add any helper methods (e.g., `CompliancePolicy::is_compliant(&self, license: &str) -> bool`)

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with methods to generate compliance reports

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) — the service takes a database connection pool and provides async methods returning `Result<T, AppError>`.
- Use SeaORM queries against the existing `package_license` entity (`entity/src/package_license.rs`) to retrieve license mappings for packages in the SBOM.
- Walk transitive dependencies through the `sbom_package` entity (`entity/src/sbom_package.rs`) — this join table links SBOMs to their packages, including transitive dependencies ingested during SBOM processing.
- Group packages by license identifier, then evaluate each group against the `CompliancePolicy` to set the `compliant` flag.
- Load the `CompliancePolicy` from the JSON config file at service initialization or per-request (consider caching for performance).
- Use the query builder helpers from `common/src/db/query.rs` for any filtering or pagination needs.
- Wrap all database errors with `.context()` per the error handling convention — all functions return `Result<T, AppError>` using the `AppError` enum from `common/src/error.rs`.
- Per CONVENTIONS.md Key Conventions: use SeaORM for database queries and follow the module pattern (model/ + service/ + endpoints/). Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust module scope.
- Per CONVENTIONS.md Key Conventions: use shared query helpers from `common/src/db/query.rs` for filtering and sorting. Applies: task modifies service code that queries the database matching the convention's query helper scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference for service pattern, database connection handling, and error wrapping
- `modules/fundamental/src/package/service/mod.rs::PackageService` — reference for querying package data
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting
- `common/src/error.rs::AppError` — error type with `IntoResponse` implementation
- `entity/src/package_license.rs` — Package-License mapping entity for SeaORM queries
- `entity/src/sbom_package.rs` — SBOM-Package join table for dependency tree traversal

## Acceptance Criteria
- [ ] `LicenseReportService` exists with a method to generate a `LicenseReport` for a given SBOM ID
- [ ] Packages are grouped by license identifier (e.g., all MIT packages in one group)
- [ ] Transitive dependencies are included in the report (not just direct dependencies)
- [ ] Each license group has a `compliant` flag set based on the loaded `CompliancePolicy`
- [ ] Denied licenses are flagged as `compliant: false`
- [ ] Allowed-only policies flag unlisted licenses as `compliant: false`
- [ ] Database errors are wrapped with `.context()` and returned as `AppError`
- [ ] Report generation meets p95 < 500ms for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Service returns a LicenseReport with packages grouped by license for a valid SBOM
- [ ] Service includes transitive dependency licenses in the report
- [ ] Service correctly applies denied license policy (denied license results in `compliant: false`)
- [ ] Service correctly applies allowed license policy (unlisted license results in `compliant: false`)
- [ ] Service returns an appropriate error for a non-existent SBOM ID
- [ ] Service handles SBOMs with no packages gracefully (empty groups)

## Dependencies
- Depends on: Task 1 — Add license report model and policy types
