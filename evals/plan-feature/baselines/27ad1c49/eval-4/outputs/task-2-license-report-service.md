## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license compliance report service that aggregates package-license data for a given SBOM, walks the full dependency tree to include transitive dependencies, groups packages by license type, and checks each group against the configured license policy to set compliance flags.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod license_report;` declaration and integrate the license report method into SbomService

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — implement the license report generation logic: query package-license data via SeaORM, walk the dependency tree using sbom_package relations, group by license, evaluate compliance against LicensePolicy

## Implementation Notes
- Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs` for method signatures and error handling (return `Result<T, AppError>` with `.context()` wrapping).
- Use the existing `entity/src/package_license.rs` entity to query the license mapping for packages in the SBOM.
- Use `entity/src/sbom_package.rs` to find all packages (including transitive dependencies) linked to the given SBOM.
- Use `common/src/db/query.rs` query builder helpers for constructing the database queries.
- The service method should accept the SBOM ID and a reference to a loaded LicensePolicy, then return a LicenseComplianceReport.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use a single query with JOINs across sbom_package and package_license rather than N+1 queries.
- No new database tables — aggregate exclusively from existing package and package_license data.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — follow its patterns for database access, connection handling, and error wrapping
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/package_license.rs` — the Package-License mapping entity for querying license data
- `entity/src/sbom_package.rs` — SBOM-Package join table for finding all packages in an SBOM

## Acceptance Criteria
- [ ] Service method accepts an SBOM ID and returns a LicenseComplianceReport
- [ ] All packages linked to the SBOM (including transitive dependencies via sbom_package) are included
- [ ] Packages are grouped by license type
- [ ] Each group's `compliant` flag is set based on the LicensePolicy configuration
- [ ] Uses efficient JOINed queries instead of N+1 pattern
- [ ] Returns appropriate AppError when SBOM is not found

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

## Dependencies
- Depends on: Task 1 — Add license report model types and policy configuration
