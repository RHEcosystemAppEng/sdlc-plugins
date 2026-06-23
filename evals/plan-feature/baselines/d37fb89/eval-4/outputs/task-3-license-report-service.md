## Repository
trustify-backend

## Target Branch
main

## Description
Implement the core license report generation logic in the SBOM service layer. This method queries all packages for a given SBOM, resolves transitive dependencies to include their licenses, groups packages by license type, evaluates each group against the configured license policy, and returns a `LicenseReport`.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `generate_license_report()` method implementation as an extension of SbomService

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` export and integrate the method into SbomService

## Implementation Notes
The `generate_license_report()` method should:

1. Verify the SBOM exists using the existing fetch pattern in `modules/fundamental/src/sbom/service/sbom.rs::SbomService`
2. Query all packages linked to the SBOM via `entity/src/sbom_package.rs` (SBOM-Package join table)
3. For each package, fetch the license via `entity/src/package_license.rs` (Package-License mapping)
4. Walk transitive dependencies through the SBOM package relationships to include indirect dependency licenses
5. Group packages by license identifier
6. For each group, evaluate compliance using `LicensePolicy::is_compliant()` from task 2
7. Construct and return a `LicenseReport` with all groups and summary counts

Use the shared query builder helpers from `common/src/db/query.rs` for database queries. Follow the `Result<T, AppError>` return pattern with `.context()` wrapping from `common/src/error.rs`.

Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Consider batching database queries rather than N+1 per-package lookups.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service patterns for SBOM fetch and database access
- `entity/src/sbom_package.rs` — SeaORM entity for SBOM-Package join, used to find packages in an SBOM
- `entity/src/package_license.rs` — SeaORM entity for Package-License mapping, used to look up license per package
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `generate_license_report(sbom_id)` returns a `LicenseReport` with packages grouped by license
- [ ] Transitive dependency licenses are included in the report
- [ ] Each license group has a `compliant` flag based on the configured license policy
- [ ] Returns appropriate `AppError` (404) when SBOM ID does not exist
- [ ] Report includes correct `total_packages` and `non_compliant_count` summary fields
- [ ] No N+1 query patterns — package and license data fetched in batch queries

## Test Requirements
- [ ] Unit test: report groups packages correctly by license type
- [ ] Unit test: transitive dependencies are included in license groups
- [ ] Unit test: compliance flags match the configured license policy
- [ ] Unit test: non-existent SBOM ID returns 404 error
- [ ] Unit test: empty SBOM (no packages) returns empty report with zero counts

## Dependencies
- Depends on: Task 1 — Add license report model structs
- Depends on: Task 2 — Add license policy configuration and compliance evaluation

[sdlc-workflow] Description digest: sha256-md:82c956b24f88ddfca6fa193fd7bb2437eefe40d66db7108ab19950faf79fef9a
