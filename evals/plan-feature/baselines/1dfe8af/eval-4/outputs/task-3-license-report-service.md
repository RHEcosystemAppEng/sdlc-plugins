## Repository
trustify-backend

## Target Branch
main

## Description
Implement the service-layer method that generates a license compliance report for a given SBOM. This method queries the existing package-license data via SeaORM entities, groups packages by license, evaluates each group against the license policy, and returns a `LicenseReport` struct. No new database tables are needed; the method aggregates from existing `sbom_package` and `package_license` entity relationships.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — Implement `generate_license_report` method for the SBOM service

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` and wire the new method into `SbomService`

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` where `SbomService` methods accept a database connection and return `Result<T, AppError>`.
- The method signature should be: `pub async fn generate_license_report(&self, sbom_id: &str, policy: &LicensePolicy, db: &impl ConnectionTrait) -> Result<LicenseReport, AppError>`.
- Query flow:
  1. Verify the SBOM exists using the existing `sbom` entity (`entity/src/sbom.rs`).
  2. Join `sbom_package` (`entity/src/sbom_package.rs`) with `package` (`entity/src/package.rs`) and `package_license` (`entity/src/package_license.rs`) to get all packages and their licenses for the SBOM.
  3. Include transitive dependencies by walking the full dependency tree through `sbom_package` relationships.
  4. Group results by license identifier using a `HashMap<String, Vec<PackageRef>>`.
  5. For each group, call `policy.is_compliant(&license)` to set the `compliant` flag.
  6. Assemble and return the `LicenseReport`.
- Use `common/src/db/query.rs` helpers if applicable for any filtering.
- Return `AppError::NotFound` if the SBOM ID does not exist.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service with fetch/list methods; follow the same connection handling and error patterns
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Reference for querying package entities
- `entity/src/sbom_package.rs` — Join table entity for SBOM-to-package relationships
- `entity/src/package_license.rs` — Entity mapping packages to their license identifiers
- `common/src/db/query.rs` — Shared query builder helpers

## Acceptance Criteria
- [ ] `generate_license_report` returns a `LicenseReport` with packages grouped by license
- [ ] Each `LicenseGroup` has a correct `compliant` flag based on the loaded `LicensePolicy`
- [ ] Transitive dependencies are included in the report
- [ ] Returns `AppError::NotFound` for non-existent SBOM IDs
- [ ] No new database tables are created

## Test Requirements
- [ ] Unit test with mock data: SBOM with packages under MIT (allowed) and GPL-3.0 (denied) produces two groups with correct compliance flags
- [ ] Unit test: SBOM with no packages returns an empty report with zero groups
- [ ] Unit test: non-existent SBOM ID returns a NotFound error

## Dependencies
- Depends on: Task 1 — Add license report model structs
- Depends on: Task 2 — Add license policy configuration

[sdlc-workflow] Description digest: sha256-md:ccdc5f430f099f81e604de018ea6f6e07801b202a36389c7fa8710cf21f6c73f
