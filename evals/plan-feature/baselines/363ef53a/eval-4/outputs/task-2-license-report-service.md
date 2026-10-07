## Repository
trustify-backend

## Target Branch
main

## Description
Add the license report service that aggregates package license data for a given SBOM, walks the full dependency tree (including transitive dependencies), groups packages by license type, and checks each group against the configured license policy. This is the core business logic for the license compliance report feature (TC-9004). The service queries existing package and license data from the database without requiring new tables.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` -- LicenseReportService with methods: `generate_report(sbom_id, db, policy) -> Result<LicenseReport, AppError>` that queries sbom_package and package_license tables, walks the transitive dependency tree, groups results by license, and evaluates compliance

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- add `pub mod license_report;` and wire LicenseReportService into the module exports

## Implementation Notes
- Query the `sbom_package` join table to get all packages for the given SBOM ID, then join with `package_license` to get each package's license.
- For transitive dependency walking: recursively resolve packages referenced by SBOM packages. Use the existing sbom_package relationships to traverse the dependency tree. Implement iterative BFS or DFS with a visited set to avoid cycles.
- Group the collected packages by their license identifier. For each group, call `LicensePolicy::check_compliance()` to determine the `compliant` flag.
- Per CONVENTIONS.md $Error Handling: all service methods must return `Result<T, AppError>` and use `.context()` for error wrapping.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust service file scope.
  See `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for the established error handling pattern.
- Per CONVENTIONS.md $Module Pattern: follow the model/ + service/ + endpoints/ structure for service placement.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust module file scope.
  See `modules/fundamental/src/sbom/service/sbom.rs` for the established service module pattern.
- Per CONVENTIONS.md $Query Helpers: use the shared query builder helpers from `common/src/db/query.rs` for filtering and pagination if applicable.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust service file scope.
  See `common/src/db/query.rs` for the query builder helper pattern.
- No new database tables are permitted -- aggregate exclusively from existing `sbom_package` and `package_license` data.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Consider batch queries rather than N+1 patterns for the dependency tree walk.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- existing service demonstrating DB query patterns, connection handling, and error wrapping; follow its method signatures and Result<T, AppError> pattern
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- package query methods that can be reused or referenced for fetching package data
- `common/src/db/query.rs` -- shared query builder helpers for filtering and sorting; reuse for any list-style queries in the dependency walker
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity; use for dependency tree traversal queries
- `entity/src/package_license.rs` -- Package-License mapping entity; use for license data retrieval

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report()` returns a `LicenseReport` with packages grouped by license
- [ ] Transitive dependencies are included in the report (not just direct SBOM packages)
- [ ] Each `LicenseGroup` has a correct `compliant` flag based on the loaded `LicensePolicy`
- [ ] Packages with unknown or missing licenses are grouped under an "Unknown" license group and flagged as non-compliant
- [ ] The service does not create or modify any database tables

## Test Requirements
- [ ] Unit test: service correctly groups packages by license from mock data
- [ ] Unit test: service walks transitive dependencies and includes them in the report
- [ ] Unit test: service correctly flags non-compliant licenses based on policy
- [ ] Unit test: service handles SBOMs with no packages (returns empty report)
- [ ] Unit test: service handles packages with no license data (groups under "Unknown")
- [ ] Unit test: service handles circular dependencies without infinite loops

## Verification Commands
- `cargo build -p trustify-module-fundamental` -- builds without errors
- `cargo test -p trustify-module-fundamental -- license_report` -- all unit tests pass

## Dependencies
- Depends on: Task 1 -- Add license policy configuration and report models
