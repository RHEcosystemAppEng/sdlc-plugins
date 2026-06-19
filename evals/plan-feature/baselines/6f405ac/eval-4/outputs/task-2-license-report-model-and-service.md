## Repository
trustify-backend

## Target Branch
main

## Description
Create the license report model and service that aggregates package-license data from existing database entities, walks transitive dependencies, groups packages by license type, and flags non-compliant licenses using the LicensePolicyService from Task 1. No new database tables are required -- the service queries existing package, sbom_package, and package_license entities.

## Files to Create
- `modules/fundamental/src/sbom/license_report/model/report.rs` — LicenseReportGroup struct (license identifier, list of packages, compliant flag) and LicenseReport struct (list of groups)
- `modules/fundamental/src/sbom/license_report/service/report.rs` — LicenseReportService: query packages for an SBOM, walk transitive dependencies, group by license, evaluate compliance via LicensePolicyService

## Files to Modify
- `modules/fundamental/src/sbom/license_report/model/mod.rs` — Add `pub mod report;` and re-export report types
- `modules/fundamental/src/sbom/license_report/service/mod.rs` — Add `pub mod report;` and re-export LicenseReportService

## Implementation Notes
The report aggregates from existing entities. Use the SeaORM entity definitions in:
- `entity/src/sbom_package.rs` — SBOM-Package join table to find packages belonging to an SBOM
- `entity/src/package_license.rs` — Package-License mapping to get license data for each package
- `entity/src/package.rs` — Package entity for package details

The LicenseReportService should accept a database connection and an SBOM ID, then:
1. Query all packages linked to the SBOM via the sbom_package join table
2. For each package, query its licenses via the package_license mapping
3. Walk transitive dependencies (packages linked through dependency relationships)
4. Group packages by license identifier
5. For each group, evaluate compliance using LicensePolicyService

Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for database query patterns and error handling.

Use the shared query helpers from `common/src/db/query.rs` for any filtering or pagination needs.

Per CONVENTIONS.md §Module pattern: follow `model/ + service/ + endpoints/` structure. Applies: task creates `modules/fundamental/src/sbom/license_report/model/report.rs` and `modules/fundamental/src/sbom/license_report/service/report.rs` matching the convention's module directory scope.

Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/license_report/service/report.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Framework: use SeaORM for database queries. Applies: task creates `modules/fundamental/src/sbom/license_report/service/report.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service pattern for database queries against SBOM data; follow the same query and error handling patterns
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — Error type for Result returns
- `entity/src/sbom_package.rs` — SeaORM entity for SBOM-Package join; reuse for querying packages by SBOM ID
- `entity/src/package_license.rs` — SeaORM entity for Package-License mapping; reuse for querying licenses by package

## Acceptance Criteria
- [ ] LicenseReport struct contains a list of LicenseReportGroup entries
- [ ] Each LicenseReportGroup contains a license identifier, list of packages, and a boolean compliant flag
- [ ] Service correctly aggregates all packages (including transitive dependencies) for a given SBOM ID
- [ ] Packages are grouped by license identifier
- [ ] Each group's compliant flag reflects the LicensePolicyService evaluation
- [ ] Report generation completes within p95 < 500ms for SBOMs with up to 1000 packages
- [ ] Non-existent SBOM ID returns an appropriate AppError

## Test Requirements
- [ ] Unit test: report groups packages correctly by license type
- [ ] Unit test: report flags non-compliant groups based on policy
- [ ] Unit test: report includes transitive dependency packages
- [ ] Unit test: report returns error for non-existent SBOM ID

## Dependencies
- Depends on: Task 1 — License policy model and service
