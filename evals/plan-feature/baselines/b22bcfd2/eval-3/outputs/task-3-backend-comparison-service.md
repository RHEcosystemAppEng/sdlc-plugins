## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the comparison logic in SbomService that computes an on-the-fly diff between two SBOMs. This service method queries existing package, advisory, and license data for both SBOMs and computes the structured diff without creating new database tables, per the non-functional requirements.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare` method to SbomService
- `modules/fundamental/src/sbom/service/mod.rs` — export comparison-related items if needed

## Implementation Notes
Add a `pub async fn compare(&self, left_id: Uuid, right_id: Uuid, db: &DatabaseConnection) -> Result<SbomComparisonResult, AppError>` method to SbomService in `modules/fundamental/src/sbom/service/sbom.rs`.

The method should:
1. Fetch package lists for both SBOMs using the SBOM-Package join table (`entity/src/sbom_package.rs`) — query packages linked to each SBOM ID
2. Compute set differences: added = right - left, removed = left - right, version_changes = intersection with different versions
3. For each package, look up license info via `entity/src/package_license.rs` to populate license fields and detect license changes
4. Query advisories for both SBOMs using `entity/src/sbom_advisory.rs` — compute new_vulnerabilities (in right, not in left) and resolved_vulnerabilities (in left, not in right)
5. Use advisory severity from the AdvisoryService pattern in `modules/fundamental/src/advisory/service/advisory.rs`

Follow the error handling pattern from existing SbomService methods: use `Result<T, AppError>` with `.context()` wrapping from `common/src/error.rs`.

Use query helpers from `common/src/db/query.rs` for database operations. Do not create new database tables — all data is computed from existing entities.

Performance target: p95 < 1s for SBOMs with up to 2000 packages each. Use efficient set operations (HashMaps keyed by package name) rather than nested loops.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct to extend with compare method
- `modules/fundamental/src/package/service/mod.rs::PackageService` — reference for querying package data
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference for querying advisory data
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error handling enum

## Acceptance Criteria
- [ ] SbomService has a `compare` method accepting two SBOM IDs
- [ ] Method returns SbomComparisonResult with all six diff categories populated correctly
- [ ] Diff is computed on-the-fly from existing data without new database tables
- [ ] Method handles case where one or both SBOM IDs don't exist (returns appropriate error)
- [ ] Performance: efficient set operations using HashMaps, not nested loops

## Test Requirements
- [ ] Unit test: comparing two identical SBOMs returns empty diff in all categories
- [ ] Unit test: adding a package to right SBOM shows it in added_packages
- [ ] Unit test: removing a package from right SBOM shows it in removed_packages
- [ ] Unit test: changing a package version shows it in version_changes with correct direction
- [ ] Unit test: new advisory in right SBOM shows in new_vulnerabilities
- [ ] Unit test: advisory only in left SBOM shows in resolved_vulnerabilities
- [ ] Unit test: license change between SBOMs shows in license_changes
- [ ] Unit test: non-existent SBOM ID returns error

## Dependencies
- Depends on: Task 2 — Backend comparison model
