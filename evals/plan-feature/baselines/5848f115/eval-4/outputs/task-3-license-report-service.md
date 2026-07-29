# Task 3 -- Add license report service

## Repository
trustify-backend

## Target Branch
main

## Description
Add a service that generates license compliance reports for a given SBOM. The service aggregates package-license data from existing entities, walks the full transitive dependency tree via sbom_package relationships, evaluates each license against the configured policy, and returns a structured LicenseReport grouped by license type.

This is the core business logic for the feature. The NFR requires p95 < 500ms for SBOMs with up to 1000 packages, so the implementation must use efficient database queries rather than N+1 patterns.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` -- LicenseReportService with report generation logic

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- Add `pub mod license_report;` to expose the new service module

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: generates and returns a license compliance report for the specified SBOM (endpoint handler in Task 4; this task provides the service layer)

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/` -- see `sbom.rs` (SbomService) for the established service pattern: struct with database connection, methods returning `Result<T, AppError>`.
- The `LicenseReportService` should implement a method like:
  ```
  pub async fn generate_report(&self, sbom_id: &str, policy: &LicensePolicy) -> Result<LicenseReport, AppError>
  ```
- **Transitive dependency walk**: query `sbom_package` join table to get all packages linked to the SBOM (direct and transitive). The `sbom_package` entity in `entity/src/sbom_package.rs` provides the SBOM-to-package relationship. Use a single query joining `sbom_package` -> `package` -> `package_license` to fetch all package-license pairs for the SBOM.
- **Grouping**: group packages by their license identifier from `package_license` (entity defined in `entity/src/package_license.rs`). Each group becomes a `LicenseReportGroup`.
- **Compliance evaluation**: for each license group, call `LicensePolicy::is_compliant()` from Task 1 to set the `compliant` flag.
- **Performance**: use a single aggregating query rather than per-package queries to meet the p95 < 500ms NFR. Use `common/src/db/query.rs` query builder helpers if applicable for constructing the join query.
- Error handling: wrap all database errors with `.context()` per project conventions, returning `AppError`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs` -- SbomService implementation; follow the same struct + async method pattern with database connection handling
- `common/src/db/query.rs` -- Shared query builder helpers for filtering, pagination, and sorting; may be useful for constructing the aggregation query
- `entity/src/package_license.rs` -- Package-License mapping entity; the data source for license information
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity; provides the relationship for fetching all packages in an SBOM (including transitive dependencies)
- `entity/src/package.rs` -- Package entity; provides package name and version data

## Acceptance Criteria
- [ ] Service correctly aggregates all packages in an SBOM grouped by license type
- [ ] Transitive dependency licenses are included (full dependency tree walk via sbom_package)
- [ ] Each license group has the correct `compliant` flag based on the configured policy
- [ ] Service handles SBOMs with no packages gracefully (returns empty groups list)
- [ ] Service handles packages with no license data gracefully (groups them under an "Unknown" license)

## Test Requirements
- [ ] Unit test: service groups packages by license correctly
- [ ] Unit test: service includes transitive dependencies (packages linked via sbom_package)
- [ ] Unit test: service evaluates compliance correctly against a test policy (allowed, denied, and default cases)
- [ ] Unit test: service returns empty groups for an SBOM with no packages
- [ ] Unit test: service handles packages with missing license data (grouped under "Unknown")
- [ ] Performance test: verify report generation completes within 500ms for an SBOM with 1000 packages

## Verification Commands
- `cargo test -p fundamental` -- all tests pass including new license report service tests

## Dependencies
- Depends on: Task 1 -- Add license policy configuration model and loader (provides `LicensePolicy` for compliance evaluation)
- Depends on: Task 2 -- Add license compliance report model (provides `LicenseReport` and `LicenseReportGroup` response types)
