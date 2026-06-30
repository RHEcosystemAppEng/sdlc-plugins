# Task 2 -- Add license report model and service

## Repository
trustify-backend

## Target Branch
main

## Description
Add the license report domain model and service layer that aggregates package license data from an SBOM, groups packages by license type, walks transitive dependencies, and flags non-compliant licenses based on the license policy configuration. This implements the core business logic for the license compliance report feature (TC-9004).

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- LicenseReportGroup struct (license name, list of packages, compliant flag) and LicenseReport struct (list of groups, overall compliance status)
- `modules/fundamental/src/sbom/service/license_report.rs` -- LicenseReportService with a `generate_report(sbom_id, policy)` method that queries existing package-license data, walks transitive dependencies, groups by license, and applies policy checks

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod license_report;` to expose the new model
- `modules/fundamental/src/sbom/service/mod.rs` -- Add `pub mod license_report;` to expose the new service module

## API Changes
- None (this task adds internal service logic only; the endpoint is added in Task 3)

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/` -- see `summary.rs` (SbomSummary) and `details.rs` (SbomDetails) for struct patterns and derive attributes.
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/` -- see `sbom.rs` (SbomService) for how services query the database and return typed results.
- The service should use the existing `package_license` entity (`entity/src/package_license.rs`) to fetch license data for packages in the SBOM.
- Use `sbom_package` entity (`entity/src/sbom_package.rs`) to get the list of packages for a given SBOM.
- For transitive dependency walking: query the `sbom_package` join table to get all packages (direct and transitive) linked to the SBOM, then fetch their licenses via `package_license`.
- Use shared query helpers from `common/src/db/query.rs` for building database queries.
- All service methods should return `Result<T, AppError>` with `.context()` wrapping, consistent with the error handling pattern in `common/src/error.rs`.
- The `LicenseReportGroup` struct should serialize to the response shape specified in the feature requirements: `{ license: "MIT", packages: [...], compliant: true }`.
- Per CONVENTIONS.md (repository conventions): follow the `model/ + service/ + endpoints/` module pattern.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust module scope.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use batch queries rather than N+1 queries when fetching package licenses.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- Reference for database query patterns, service method signatures, and error handling within the sbom module.
- `entity/src/package_license.rs` -- Existing entity for package-to-license mapping; use directly rather than creating new queries.
- `entity/src/sbom_package.rs` -- Existing join table entity for SBOM-to-package relationships; use to enumerate packages in an SBOM.
- `common/src/db/query.rs` -- Shared query builder helpers for filtering and pagination.
- `common/src/model/license_policy.rs::LicensePolicy` -- The policy model created in Task 1; use to check compliance of each license group.

## Acceptance Criteria
- [ ] A `LicenseReport` model struct exists with groups of packages organized by license type
- [ ] Each group contains a `compliant` flag based on the license policy
- [ ] The service aggregates licenses from all packages in the SBOM, including transitive dependencies
- [ ] The service returns a complete `LicenseReport` for a given SBOM ID
- [ ] Non-compliant licenses (per the policy) are correctly flagged with `compliant: false`

## Test Requirements
- [ ] Unit test: generate a report for an SBOM with packages having a single known-compliant license (e.g., MIT) -- verify all groups are compliant
- [ ] Unit test: generate a report for an SBOM with a non-compliant license -- verify the group is flagged as non-compliant
- [ ] Unit test: generate a report for an SBOM with transitive dependencies -- verify transitive package licenses are included
- [ ] Unit test: generate a report for an SBOM with no packages -- verify empty groups list is returned
- [ ] Unit test: verify performance is acceptable with a large package set (benchmark or assert query count)

## Dependencies
- Depends on: Task 1 -- Add license policy configuration model and loader

<!-- [sdlc-workflow] Description digest: sha256-md:c0c645dd775ddc3fc9a3db3c52695e796d36d9fc1bb53b6db97a22334be1ce20 -->
