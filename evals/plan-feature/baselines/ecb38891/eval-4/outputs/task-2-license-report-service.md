## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service that aggregates license data from all packages in an SBOM (including transitive dependencies), groups packages by license type, and checks each group against the license policy for compliance. The service walks the full dependency tree to include transitive dependency licenses, ensuring complete coverage of all open-source components.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with methods to generate a LicenseReport for a given SBOM ID, including transitive dependency tree walk and policy compliance checking

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod license_report;` module declaration

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) — accept a database connection pool and expose async methods returning `Result<T, AppError>`.
- Per Key Conventions §Module pattern: follow the `model/ + service/ + endpoints/` structure. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's service directory scope.
- Per Key Conventions §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping for database and I/O errors. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` which performs database queries and policy loading.
- Use the `sbom_package` join table (`entity/src/sbom_package.rs`) to find all packages belonging to the SBOM, then use the `package_license` table (`entity/src/package_license.rs`) to retrieve license data for each package.
- For transitive dependency resolution: query all packages linked to the SBOM via `sbom_package`, then recursively resolve their dependencies. If the existing schema does not support recursive dependency resolution, use a breadth-first traversal over the package relationships.
- Group the resulting packages by their license identifier (SPDX format), creating one LicenseGroup per unique license.
- Apply the LicensePolicy from Task 1 to flag each group's `compliant` field.
- Use `common/src/db/query.rs` query builder helpers for constructing efficient database queries.
- Performance requirement: p95 < 500ms for SBOMs with up to 1000 packages. Consider batch-loading license data rather than N+1 queries — load all package-license mappings for the SBOM in a single query, then group in-memory.

## Reuse Candidates
- `entity/src/sbom_package.rs::SbomPackage` — SBOM-Package join table entity for querying packages within an SBOM
- `entity/src/package_license.rs::PackageLicense` — Package-License mapping for retrieving license data per package
- `entity/src/package.rs::Package` — Package entity for dependency relationship traversal
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse for efficient license data queries
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — follow the same service structure pattern (constructor, async methods, error handling)

## Acceptance Criteria
- [ ] LicenseReportService generates a LicenseReport for a valid SBOM ID
- [ ] Report includes all direct dependency packages with their licenses
- [ ] Report includes transitive dependency packages with their licenses
- [ ] Packages are grouped by license type (one LicenseGroup per unique license)
- [ ] Each LicenseGroup has a correct `compliant` flag based on the license policy
- [ ] Service returns an appropriate error for non-existent SBOM IDs
- [ ] Performance: report generation completes within 500ms for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Unit test: service groups packages by license correctly
- [ ] Unit test: service includes transitive dependencies in the report
- [ ] Unit test: service applies policy compliance flags correctly
- [ ] Unit test: service returns error for non-existent SBOM ID
- [ ] Unit test: service handles SBOM with no packages (empty report)
- [ ] Unit test: service handles packages with no license data gracefully

## Dependencies
- Depends on: Task 1 — Add license policy configuration and license report models
