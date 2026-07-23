# Task 3 — Add license report service with transitive dependency resolution

**Summary:** Add license report service with transitive dependency resolution

**Epic:** TC-9004: License report service and API

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the core license report service that aggregates package licenses from an SBOM, walks the transitive dependency tree to include indirect dependency licenses, groups packages by license type, and checks each group against the configured license policy. This service is the business logic layer consumed by the REST endpoint (Task 4).

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — defines `LicenseReportService` with a `generate_report(sbom_id)` method that produces a `LicenseReport`

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod license_report` to register the new service module

## Implementation Notes
- Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`). The service should accept a database connection and the license policy as dependencies.
- **Data aggregation strategy** (no new tables required):
  1. Query `sbom_package` join table to get all direct packages for the given SBOM ID
  2. For each package, query `package_license` entity to get its license(s)
  3. Walk transitive dependencies by recursively following package dependency relationships through `sbom_package` (packages that are dependencies of other packages in the same SBOM)
  4. Group all collected packages by their license SPDX identifier
  5. For each group, call `LicensePolicy::is_compliant()` to set the compliance flag
- Use the query builder helpers from `common/src/db/query.rs` for database queries, consistent with other service implementations.
- Use SeaORM entities from `entity/src/`:
  - `entity/src/sbom_package.rs` — SBOM-Package join table for direct package lookup
  - `entity/src/package_license.rs` — Package-License mapping for license data
  - `entity/src/package.rs` — Package entity for package details
- Return `Result<LicenseReport, AppError>` following the error pattern from `common/src/error.rs`.
- **Performance consideration**: the NFR specifies p95 < 500ms for SBOMs with up to 1000 packages. Use batch queries rather than N+1 individual lookups. Load all packages and their licenses in bulk, then perform grouping in memory.
- Mark each `PackageLicenseEntry` with `transitive: true` or `transitive: false` to distinguish direct from transitive dependencies in the report.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — demonstrates the service struct pattern, database connection handling, and error propagation
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse for constructing the package/license queries
- `entity/src/package_license.rs` — existing SeaORM entity for Package-License mapping; use directly for license lookups
- `entity/src/sbom_package.rs` — existing SeaORM entity for SBOM-Package join; use for package enumeration

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report(sbom_id)` returns a `LicenseReport` with packages grouped by license
- [ ] Direct dependency packages are included with `transitive: false`
- [ ] Transitive dependency packages are included with `transitive: true`
- [ ] Each license group has a correct `compliant` flag based on the loaded policy
- [ ] Service returns an appropriate error when the SBOM ID does not exist
- [ ] Report generation completes within performance targets (p95 < 500ms for 1000 packages)

## Test Requirements
- [ ] Test report generation for an SBOM with packages having various licenses (MIT, Apache-2.0, GPL-3.0)
- [ ] Test that transitive dependencies are included in the report
- [ ] Test that compliance flags correctly reflect the policy (allowed licenses are compliant, denied are not)
- [ ] Test error handling for a non-existent SBOM ID
- [ ] Test report generation for an SBOM with no packages (empty groups)

## Dependencies
- Depends on: Task 1 — Add license report response model types
- Depends on: Task 2 — Add license policy configuration and loader
