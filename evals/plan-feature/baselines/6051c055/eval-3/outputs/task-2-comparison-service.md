# Task 2 -- SBOM comparison service

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the comparison diff logic in SbomService that computes a structured diff between two SBOMs. The service queries existing package, advisory, and license data for both SBOMs and produces an SbomComparisonResult with added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The diff is computed on-the-fly with no new database tables, and must meet the p95 < 1s performance target for SBOMs with up to 2000 packages.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- Add `compare(&self, left_id: &str, right_id: &str, db: &DatabaseConnection) -> Result<SbomComparisonResult, AppError>` method to SbomService

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for method signatures, database access, and error handling.
- Load packages for both SBOMs using existing queries against `entity/src/sbom_package.rs` (sbom_package table). Build HashMaps keyed by package name for efficient diffing.
- Compute added_packages: packages in right SBOM but not in left. Compute removed_packages: packages in left SBOM but not in right. Compute version_changes: packages in both SBOMs with different versions, including direction ("upgrade" or "downgrade") via version string comparison.
- For vulnerability diffing, query advisories associated with each SBOM's packages. new_vulnerabilities: advisories affecting right-only packages. resolved_vulnerabilities: advisories affecting left-only packages.
- For license changes, query `entity/src/package_license.rs` (package_license table) and compare licenses for packages present in both SBOMs.
- Use batch queries rather than per-package queries to meet the p95 < 1s latency target for 2000-package SBOMs.
- Return `AppError::NotFound` from `common/src/error.rs` if either SBOM ID does not exist.
- Per CONVENTIONS.md Error Handling: wrap all fallible operations with `.context()` and return `Result<T, AppError>`. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` scope.

## Acceptance Criteria
- [ ] SbomService::compare() method is implemented and returns SbomComparisonResult
- [ ] Added and removed packages are correctly computed from package set differences
- [ ] Version changes include direction field ("upgrade" or "downgrade")
- [ ] New and resolved vulnerabilities are computed from advisory associations
- [ ] License changes are computed for packages present in both SBOMs
- [ ] Returns AppError::NotFound when either SBOM ID does not exist
- [ ] p95 latency < 1s for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package differences produces correct added/removed sets
- [ ] Unit test: compare identical SBOMs returns all-empty diff sections
- [ ] Unit test: version change direction is correctly determined

## Dependencies
- Depends on: Task 1 -- SBOM comparison data model
