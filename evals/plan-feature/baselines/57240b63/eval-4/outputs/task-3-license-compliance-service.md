## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license compliance service that aggregates package license data from an SBOM's full dependency tree and evaluates each license against the configured policy. The service produces a LicenseReport with packages grouped by license type and compliance flags. This is the core business logic for the license compliance report feature.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` -- LicenseReportService with report generation logic

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- add `pub mod license_report;` to expose the new service module

## Implementation Notes
- Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for struct layout, database connection handling, and error propagation.
- The service method `generate_report(db: &DatabaseConnection, sbom_id: Id, policy: &LicensePolicy) -> Result<LicenseReport, AppError>` should:
  1. Query `entity/src/sbom_package.rs` join table to get all packages linked to the SBOM, including transitive dependencies via the full dependency tree.
  2. Query `entity/src/package_license.rs` to get license mappings for each package.
  3. Group packages by SPDX license identifier into `LicenseGroup` entries.
  4. Evaluate each group's compliance using `LicensePolicy::is_compliant()`.
  5. Set the top-level `LicenseReport.compliant` to `false` if any group is non-compliant.
  6. Return the assembled `LicenseReport`.
- Performance requirement: p95 < 500ms for SBOMs with up to 1000 packages. Achieve this by:
  - Using a single JOIN query across sbom_package and package_license tables instead of N+1 individual lookups.
  - Collecting all package-license pairs in one database round-trip, then grouping in memory.
- Use `common/src/db/query.rs` helpers for building the database query.
- No new database tables are required -- aggregate exclusively from existing `sbom_package` and `package_license` entity data.

- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` from all service methods and use `.context()` wrapping for database query errors.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust service file scope.

- Per CONVENTIONS.md §Module Pattern: place the service logic in the service/ subdirectory following the model/ + service/ + endpoints/ structure.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's service directory scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- reference for service struct pattern, database connection handling, and query execution
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- reference for package-related query patterns
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity for dependency tree traversal
- `entity/src/package_license.rs` -- Package-License mapping entity for license data retrieval
- `common/src/model/license_policy.rs::LicensePolicy` -- policy evaluation logic (from Task 2)

## Acceptance Criteria
- [ ] Service accepts an SBOM ID and returns a `LicenseReport`
- [ ] All packages in the SBOM's dependency tree (including transitive dependencies) are included
- [ ] Packages are correctly grouped by SPDX license identifier
- [ ] Each license group has a `compliant` flag based on the configured policy
- [ ] The overall `LicenseReport.compliant` flag is `false` if any group is non-compliant
- [ ] Report generation does not create or require new database tables
- [ ] Batch JOIN queries are used to avoid N+1 query patterns

## Test Requirements
- [ ] Unit test: service correctly groups packages by license identifier
- [ ] Unit test: service flags non-compliant licenses based on policy (denied license -> compliant: false)
- [ ] Unit test: service sets overall compliance to false when any group is non-compliant
- [ ] Unit test: service includes transitive dependencies in the report
- [ ] Unit test: service returns an appropriate AppError for a non-existent SBOM ID

## Verification Commands
- `cargo check -p trustify-module-fundamental` -- expected: compiles without errors
- `cargo test -p trustify-module-fundamental` -- expected: all tests pass

## Dependencies
- Depends on: Task 1 -- License report model types
- Depends on: Task 2 -- License policy configuration

---

[sdlc-workflow] Description digest: sha256-md:43356b4b200a6f05e51805f843058674e2d56f5fd340a5758ef9856a780b1677
