## Repository
trustify-backend

## Target Branch
main

## Description
Add the license compliance report service that generates a complete license report for a given SBOM. The service aggregates package-license data from existing database entities, walks the full transitive dependency tree to include indirect dependency licenses, groups packages by license type, and checks each group against the configured license policy to determine compliance status.

This service is the core business logic layer for the license compliance report feature. It is consumed by the license report endpoint (Task 4).

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` -- implements the LicenseReportService with methods to generate the compliance report

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- add `pub mod license_report;` and integrate LicenseReportService

## API Changes
- Internal service API (not REST): `LicenseReportService::generate_report(sbom_id: Id, db: &Database, policy: &LicensePolicy) -> Result<LicenseReportResponse, AppError>` -- NEW

## Implementation Notes
- Follow the service patterns established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for method signatures, database access patterns, and error handling.
- Use SeaORM queries against the existing `entity/src/package_license.rs` (Package-License mapping) and `entity/src/sbom_package.rs` (SBOM-Package join table) entities to fetch license data for all packages in the SBOM.
- For transitive dependency resolution: query `sbom_package` relationships recursively to walk the full dependency tree. Use the existing SBOM-Package join table which already captures the dependency graph from SBOM ingestion.
- Group the results by license identifier (e.g., SPDX ID) and create a `LicenseGroup` for each unique license.
- For each group, call `LicensePolicy::is_compliant()` to set the `compliant` flag.
- Performance requirement: p95 < 500ms for SBOMs with up to 1000 packages. Consider using a single database query with JOINs rather than N+1 queries. Use the query builder helpers in `common/src/db/query.rs` where applicable.
- No new database tables are allowed -- aggregate exclusively from existing entities.
- Per CONVENTIONS.md Module pattern: follow the `model/ + service/ + endpoints/` structure.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's module directory structure scope.
- Per CONVENTIONS.md Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` handler/service scope.

### Constraints (from docs/constraints.md)
- SS5.1: Keep changes scoped to the files listed in Files to Modify and Files to Create.
- SS5.2: Inspect existing service code before writing to follow established patterns.
- SS5.3: Follow the patterns referenced in Implementation Notes.
- SS5.4: Reuse existing query helpers and entity definitions -- do not duplicate.
- SS2.1: Commit must reference Jira issue ID in footer.
- SS2.2: Use Conventional Commits format.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- reference for service method signatures, database access patterns, and error handling conventions
- `entity/src/package_license.rs` -- Package-License mapping entity, provides the license data for each package
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity, provides the relationship between SBOMs and packages (including dependency graph)
- `common/src/db/query.rs` -- shared query builder helpers for constructing efficient database queries
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- reference for querying package data

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report()` returns a `LicenseReportResponse` with packages grouped by license
- [ ] Transitive dependencies are included in the report (not just direct dependencies)
- [ ] Each license group has a `compliant` flag set based on the configured `LicensePolicy`
- [ ] No new database tables or migrations are created
- [ ] Service handles SBOMs with no packages gracefully (returns empty groups)
- [ ] Service returns appropriate error when SBOM ID does not exist

## Test Requirements
- [ ] Unit/integration test: generate report for SBOM with packages having different licenses, verify grouping
- [ ] Unit/integration test: verify transitive dependencies appear in the report
- [ ] Unit/integration test: verify compliance flags match the configured policy (allowed = true, denied = false)
- [ ] Unit/integration test: verify empty SBOM returns empty groups list
- [ ] Unit/integration test: verify non-existent SBOM ID returns error

## Verification Commands
- `cargo test -p trustify-module-fundamental -- license_report` -- run license report service tests

## Dependencies
- Depends on: Task 1 -- Add license report response model types
- Depends on: Task 2 -- Add license policy configuration
