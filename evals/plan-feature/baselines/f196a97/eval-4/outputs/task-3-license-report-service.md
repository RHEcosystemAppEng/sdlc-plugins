# Task 3 — Add license report service with compliance checking

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the LicenseReportService that generates a license compliance report for a given SBOM. The service queries all packages associated with the SBOM (including transitive dependencies), groups them by license type, and checks each group against the configured license policy to determine compliance. This is the core business logic for the license compliance report feature.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with report generation logic

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to export the new service module
- `modules/fundamental/Cargo.toml` — Add dependency on `common` crate if not already present (for LicensePolicy access)

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) — accept a database connection/pool and return `Result<T, AppError>`
- The service method signature should be approximately: `async fn generate_report(&self, sbom_id: Uuid, policy: &LicensePolicy, db: &impl ConnectionTrait) -> Result<LicenseReport, AppError>`
- Query the `sbom_package` join table (`entity/src/sbom_package.rs`) to get all packages for the SBOM, then join with `package_license` (`entity/src/package_license.rs`) to get license data
- **Transitive dependency traversal:** Walk the full dependency tree by recursively following package relationships through `sbom_package`. Use a CTE (Common Table Expression) or iterative query to collect transitive dependencies. Consider using SeaORM's `find_with_related` or raw SQL for the recursive query
- **License grouping:** Group packages by their license SPDX identifier, creating one LicenseGroup per unique license
- **Compliance checking:** For each license group, check the license against the LicensePolicy's allowed/denied lists and set the `compliant` flag accordingly
- **Performance:** Target p95 < 500ms for SBOMs with up to 1000 packages. Fetch all package-license data in a single query (or minimal queries) rather than N+1 queries. Consider using a single JOIN query across sbom_package and package_license
- Use `common/src/error.rs::AppError` with `.context()` wrapping for all error handling, consistent with the existing codebase pattern
- Aggregate from existing data — do not create new database tables

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Follow its service pattern (constructor, method signatures, error handling)
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Reference for how package queries are structured
- `common/src/db/query.rs` — Shared query builder helpers; check for reusable filtering or join utilities
- `entity/src/sbom_package.rs` — SBOM-Package join table entity; key to the package lookup query
- `entity/src/package_license.rs` — Package-License mapping entity; essential for license data retrieval

## Acceptance Criteria
- [ ] Service generates a correct LicenseReport for a given SBOM ID
- [ ] Packages are grouped by license with correct compliance flags based on the policy
- [ ] Transitive dependencies are included in the report (full dependency tree walk)
- [ ] Packages with licenses in the denied list are flagged as non-compliant
- [ ] Packages with licenses in the allowed list are flagged as compliant
- [ ] Report generation completes within 500ms for SBOMs with 1000 packages
- [ ] Returns appropriate AppError when SBOM ID is not found

## Test Requirements
- [ ] Integration test: generate report for an SBOM with packages having various licenses, verify correct grouping
- [ ] Integration test: verify denied licenses produce `compliant: false` groups
- [ ] Integration test: verify allowed licenses produce `compliant: true` groups
- [ ] Integration test: verify transitive dependencies are included in the report
- [ ] Integration test: verify report for a non-existent SBOM ID returns a 404-equivalent error
- [ ] Integration test: verify report for an SBOM with no packages returns an empty groups list

## Dependencies
- Depends on: Task 1 — Add license policy configuration model
- Depends on: Task 2 — Add license report response model
