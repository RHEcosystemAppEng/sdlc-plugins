## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `compare` method on `SbomService` that computes an on-the-fly diff between two SBOMs. The method loads packages, advisories, and license data for both SBOMs and produces a `SbomComparisonResult` with added/removed packages, version changes, new/resolved vulnerabilities, and license changes. No new database tables — the diff is computed from existing entity data.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare(left_id, right_id) -> Result<SbomComparisonResult, AppError>` method to `SbomService`

## Implementation Notes
The existing `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` provides `fetch` and `list` methods. Add a `compare` method following the same patterns:
- Use the existing entity models: `entity/src/sbom_package.rs` (SBOM-Package join table), `entity/src/package.rs` (Package entity with name/version), `entity/src/package_license.rs` (Package-License mapping), `entity/src/sbom_advisory.rs` (SBOM-Advisory join table), `entity/src/advisory.rs` (Advisory entity with severity)
- Load packages for both SBOMs via SeaORM queries on the `sbom_package` join table, joining to `package` for name/version and `package_license` for license info
- Compute set differences:
  - Added packages: packages in right SBOM not in left (by package name)
  - Removed packages: packages in left SBOM not in right (by package name)
  - Version changes: packages in both with different versions
  - New vulnerabilities: advisories linked to right SBOM packages not linked to left SBOM packages (via `sbom_advisory`)
  - Resolved vulnerabilities: advisories linked to left SBOM packages not linked to right SBOM packages
  - License changes: packages in both with different licenses
- For performance (p95 < 1s for 2000 packages per SBOM), load all packages for each SBOM in a single query and compute diffs in memory using `HashMap` keyed by package name
- Use `common/src/db/query.rs` query builder helpers for consistent query construction
- Error handling: return `AppError` with `.context("Comparing SBOMs")` if either SBOM ID is not found

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::fetch` — existing method for fetching a single SBOM, use to validate SBOM IDs exist
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package querying service, reference for SeaORM query patterns on package entities
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `SbomService::compare(left_id, right_id)` returns a `SbomComparisonResult`
- [ ] Added packages are correctly identified (present in right, absent in left)
- [ ] Removed packages are correctly identified (present in left, absent in right)
- [ ] Version changes are detected for packages present in both SBOMs with different versions
- [ ] New vulnerabilities are identified via advisory-SBOM relationships
- [ ] Resolved vulnerabilities are identified via advisory-SBOM relationships
- [ ] License changes are detected for packages with different licenses
- [ ] Returns 404 AppError if either SBOM ID does not exist
- [ ] Diff computation handles SBOMs with up to 2000 packages each within p95 < 1s

## Test Requirements
- [ ] Test `compare` with two SBOMs that have overlapping and non-overlapping packages
- [ ] Test `compare` with identical SBOMs returns all empty diff sections
- [ ] Test `compare` with non-existent SBOM ID returns 404 error
- [ ] Test that advisory-based vulnerability diff correctly uses SBOM-advisory relationships
- [ ] Test that license changes are detected when the same package has different licenses in each SBOM

## Dependencies
- Depends on: Task 1 — Backend comparison model
