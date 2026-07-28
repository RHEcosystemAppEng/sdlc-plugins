# Task 2 — Add license report service with dependency tree traversal

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `LicenseReportService` that generates a license compliance report for a given SBOM. The service queries the existing package-license data across the full dependency tree (including transitive dependencies), groups packages by license type, and checks each group against the configured license policy to flag non-compliant licenses.

This service is the core business logic layer for the license compliance report feature. It aggregates data from the existing `package_license` and `sbom_package` entities without requiring new database tables.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` -- `LicenseReportService` with methods to generate the compliance report for a given SBOM ID

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- Add `pub mod license_report;` to register the new service module

## API Changes
- `LicenseReportService::generate_report(sbom_id: Id) -> Result<LicenseReport, AppError>` -- NEW: generates the full license compliance report for the specified SBOM

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService). The service should accept a database connection pool and the license policy configuration.
- **Dependency tree traversal**: query `sbom_package` to get all packages associated with the SBOM (this entity already captures both direct and transitive dependencies from ingestion). Join with `package_license` to get each package's license. The SBOM ingestion process (in `modules/ingestor/src/graph/sbom/mod.rs`) already links all packages (including transitive) to the SBOM during parsing, so a flat query on `sbom_package` for the given SBOM ID retrieves the full dependency tree.
- **Grouping**: collect packages by their license identifier. For each group, create a `LicenseGroup` with the license name, the list of packages in that group, and the compliance flag from the policy check.
- **Performance**: the NFR requires p95 < 500ms for SBOMs with up to 1000 packages. Use a single query to fetch all package-license data for the SBOM (avoid N+1 queries). Consider using SeaORM's `find_with_related()` or a raw SQL join query for efficiency.
- **Error handling**: return `AppError` with `.context()` wrapping per the repository's error handling convention.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's service directory scope.
- Use `common/src/db/query.rs` query helpers if applicable for building the package-license aggregation query.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- Follow this service's structure for database access patterns, connection pool usage, and error handling
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity; use to query all packages for a given SBOM
- `entity/src/package_license.rs` -- Package-License mapping entity; use to look up each package's license
- `common/src/db/query.rs` -- Shared query builder helpers for filtering and building complex queries
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- Reference for how package data is queried from the database

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report()` returns a `LicenseReport` with packages correctly grouped by license
- [ ] Transitive dependencies are included in the report (all packages linked to the SBOM via `sbom_package`)
- [ ] Non-compliant licenses are correctly flagged based on the configured policy
- [ ] Overall compliance status is `false` when any license group is non-compliant
- [ ] The service handles SBOMs with no packages gracefully (returns empty report)
- [ ] The service returns an appropriate error for non-existent SBOM IDs

## Test Requirements
- [ ] Unit test: report groups packages by license correctly
- [ ] Unit test: policy compliance flags are set correctly for allowed and denied licenses
- [ ] Unit test: transitive dependencies are included in the report
- [ ] Unit test: empty SBOM returns an empty report with overall compliant status
- [ ] Unit test: non-existent SBOM ID returns an appropriate error

## Verification Commands
- `cargo test --package fundamental -- license_report` -- Run license report service tests

## Dependencies
- Depends on: Task 1 -- Add license report model types and policy configuration
