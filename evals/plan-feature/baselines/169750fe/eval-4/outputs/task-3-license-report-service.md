## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `LicenseReportService` that generates a license compliance report for a given SBOM. The service aggregates package license data from existing database tables, walks the full dependency tree via SBOM-package relations, groups packages by license type, and checks each group's compliance against the configured license policy.

## Files to Create
- `modules/fundamental/src/license/service/mod.rs` — `LicenseReportService` with a `generate_report(sbom_id, policy)` method

## Files to Modify
- `modules/fundamental/src/license/mod.rs` — add `service` submodule declaration

## Implementation Notes
Follow the service pattern from `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) for database access patterns and error handling.

The `generate_report` method should:
1. Query `sbom_package` to get all packages for the given SBOM ID
2. For each package, look up its license via `package_license` entity
3. Walk transitive dependencies by following package dependency relations in `sbom_package`
4. Group packages by license string (SPDX identifier)
5. For each group, check the license against `LicensePolicy` to determine compliance
6. Return a `LicenseComplianceReport` with all groups and the overall compliance flag

Use `entity/sbom_package.rs` for the SBOM-to-package join and `entity/package_license.rs` for the package-to-license mapping. Use SeaORM query patterns consistent with existing service implementations.

Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` structure.
Applies: task creates `modules/fundamental/src/license/service/mod.rs` matching the convention's Rust module scope.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping for all database operations.
Applies: task creates `modules/fundamental/src/license/service/mod.rs` matching the convention's Rust file scope.

Per CONVENTIONS.md §Query helpers: use shared query builder helpers from `common/src/db/query.rs` for filtering.
Applies: task creates `modules/fundamental/src/license/service/mod.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/package_license.rs` — existing package-license mapping entity
- `entity/sbom_package.rs` — existing SBOM-package join table entity
- `modules/fundamental/src/package/service/mod.rs::PackageService` — reference for package query patterns

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report` returns a `LicenseComplianceReport` for a valid SBOM ID
- [ ] Transitive dependencies are included in the report (not just direct packages)
- [ ] Packages are grouped by license type (SPDX identifier)
- [ ] Each group's `compliant` flag reflects the license policy check
- [ ] Overall `compliant` flag is false when any group contains a denied license
- [ ] Returns appropriate error for non-existent SBOM IDs
- [ ] Performance: handles SBOMs with up to 1000 packages within p95 < 500ms

## Test Requirements
- [ ] Unit test: report correctly groups packages by license
- [ ] Unit test: transitive dependencies are included in the report
- [ ] Unit test: compliance flags are set correctly based on policy (allowed, denied, review)
- [ ] Unit test: empty SBOM returns an empty report with `compliant: true`

## Dependencies
- Depends on: Task 1 — License policy model
- Depends on: Task 2 — License report model
