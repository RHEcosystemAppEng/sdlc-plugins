# Task 2 — Implement license compliance report service

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the service layer that generates a license compliance report for a given SBOM. The service fetches all packages associated with the SBOM (including transitive dependencies), groups them by license type, and evaluates each group against the configured license policy to determine compliance. The service must handle SBOMs with up to 1000 packages within the p95 < 500ms performance target.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add the `license_report` module declaration and re-export

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — implement `LicenseReportService` with the `generate_report` method

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for service struct layout and database interaction patterns.
- The service should accept a database connection/transaction and the SBOM ID as inputs.
- Query the `sbom_package` join table (`entity/src/sbom_package.rs`) to find all packages for the SBOM, then join with `package_license` (`entity/src/package_license.rs`) to get license information.
- For transitive dependency resolution: walk the SBOM's package dependency graph. If the `sbom_package` table includes direct and transitive dependencies (as typical in SBOM data), all linked packages are included. If a separate dependency-tree relation exists, traverse it.
- Group packages by their license SPDX identifier, creating one `LicenseReportGroup` per unique license.
- Load the `LicensePolicy` from the configured path and evaluate each group: a group is non-compliant if its license appears in `denied_licenses`, or (in allowlist mode) if its license does not appear in `allowed_licenses`.
- Use efficient batch queries rather than N+1 patterns — fetch all packages and licenses in as few queries as possible to meet the p95 < 500ms target.
- No new database tables are needed — aggregate from existing `package`, `sbom_package`, and `package_license` entities.
- Per CONVENTIONS.md §Module Pattern: place the service in `service/license_report.rs` within the SBOM module.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's service directory scope.
- Per CONVENTIONS.md §Error Handling: return `Result<LicenseReport, AppError>` with `.context()` wrapping on database and policy loading errors.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Query Helpers: use shared query builder helpers from `common/src/db/query.rs` for any filtering or pagination needs.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service demonstrating the database query pattern and error handling conventions
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package service with queries against the package entity
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/sbom_package.rs` — SeaORM entity for SBOM-package relationships
- `entity/src/package_license.rs` — SeaORM entity for package-license mappings

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report(sbom_id)` returns a `LicenseReport` with packages grouped by license
- [ ] Transitive dependencies are included in the report (full dependency tree walk)
- [ ] Each `LicenseReportGroup` has `compliant` set correctly based on the loaded license policy
- [ ] Packages with licenses in the `denied_licenses` list are flagged as non-compliant
- [ ] When `allowed_licenses` is configured, packages with licenses not in the list are flagged as non-compliant
- [ ] No new database tables are created — all data is aggregated from existing entities
- [ ] Report generation completes within p95 < 500ms for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Unit test: service correctly groups packages by license type
- [ ] Unit test: service flags denied licenses as non-compliant
- [ ] Unit test: service handles allowlist-mode policy correctly
- [ ] Unit test: service includes transitive dependencies in the report
- [ ] Unit test: service returns empty groups list for an SBOM with no packages
- [ ] Unit test: service returns error for non-existent SBOM ID

## Verification Commands
- `cargo build -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental -- license_report` — service unit tests pass

## Dependencies
- Depends on: Task 1 — Add license report model types and policy configuration
