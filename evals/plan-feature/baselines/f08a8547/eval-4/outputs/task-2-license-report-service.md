## Repository
trustify-backend

## Target Branch
main

## Description
Implement the service method that generates a license compliance report for a given SBOM. The service aggregates package license data from the existing `package_license` entity, walks the full transitive dependency tree via `sbom_package` relationships, groups packages by license type, and checks each group against the license policy for compliance. Performance target: p95 < 500ms for SBOMs with up to 1000 packages.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- add license_report module declaration or import

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` -- license report generation logic including transitive dependency resolution and policy compliance checking

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` for method signatures and error handling conventions
- Use `Result<T, AppError>` return type with `.context()` wrapping for all fallible operations
- Query `entity/src/sbom_package.rs` to get packages linked to the SBOM, then join with `entity/src/package_license.rs` to get license data
- For transitive dependency walking, recursively resolve package dependencies through the `sbom_package` join table; consider a batch CTE query for performance
- Group packages by license string, then check each group against the `LicensePolicy` to set the `compliant` flag
- NFR: target p95 < 500ms for SBOMs with up to 1000 packages -- use batch queries instead of N+1 queries for the dependency tree
- Do not create new database tables -- aggregate from existing `package_license` data
- Packages with no license data should be grouped under an "Unknown" license category
- Per CONVENTIONS.md Error handling: return `Result<T, AppError>` with `.context()` wrapping for all service methods.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md Query helpers: use shared filtering and query builder utilities from `common/src/db/query.rs` where applicable.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- existing service with fetch/list patterns to follow for method signatures and DB access
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination
- `entity/src/package_license.rs` -- existing entity for Package-License mapping (the data source for license aggregation)
- `entity/src/sbom_package.rs` -- existing entity for SBOM-Package relationships (needed for transitive dependency walking)
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- existing package service with query patterns to reference

## Acceptance Criteria
- [ ] Service method accepts an SBOM ID and returns a `LicenseReport`
- [ ] Packages are grouped by license type in the report
- [ ] Transitive dependencies are included in the report (full dependency tree walk)
- [ ] Each group's `compliant` flag reflects the license policy check
- [ ] No new database tables created -- uses existing `package_license` and `sbom_package` entities only
- [ ] Handles SBOMs with no packages gracefully (returns empty report with no groups)
- [ ] Handles packages with no license data (groups them under an "Unknown" license)

## Test Requirements
- [ ] Unit test: report groups packages correctly by license type
- [ ] Unit test: transitive dependencies are included in the report
- [ ] Unit test: compliant flag is set correctly based on policy (true for allowed, false for denied)
- [ ] Unit test: empty SBOM returns empty report with no groups
- [ ] Unit test: packages without license data are grouped under "Unknown"

## Dependencies
- Depends on: Task 1 -- Add license report model types and policy configuration
