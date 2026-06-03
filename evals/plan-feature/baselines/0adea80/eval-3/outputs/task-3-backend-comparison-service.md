# Task 3 — Add SBOM comparison service logic

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the service layer logic that computes a structured diff between two SBOMs. The service takes two SBOM IDs, fetches their package and advisory data from the database, and produces an `SbomComparisonResult` with added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The diff is computed on-the-fly from existing data without requiring new database tables.

## Files to Create
- `modules/fundamental/src/sbom/service/comparison.rs` — `SbomComparisonService` with a `compare(left_id, right_id)` method that returns `Result<SbomComparisonResult, AppError>`

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod comparison;` to expose the new service module

## Implementation Notes
- Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs` — use the same database connection handling and error wrapping with `.context()`.
- Use `SbomService` to fetch SBOM details for both left and right IDs. Return `AppError` (404) if either SBOM does not exist.
- Use `PackageService` (from `modules/fundamental/src/package/service/mod.rs`) to fetch packages for each SBOM.
- Use `AdvisoryService` (from `modules/fundamental/src/advisory/service/advisory.rs`) to fetch advisories linked to each SBOM.
- Compute diffs using set operations on package names:
  - **Added packages**: packages in right but not in left (by package name)
  - **Removed packages**: packages in left but not in right
  - **Version changes**: packages in both with different versions; determine direction by semver comparison if possible, fallback to string comparison
  - **New vulnerabilities**: advisories linked to right SBOM's packages but not linked to left SBOM's packages
  - **Resolved vulnerabilities**: advisories linked to left SBOM's packages but not linked to right SBOM's packages
  - **License changes**: packages in both with different license values
- Performance requirement: p95 < 1s for SBOMs with up to 2000 packages each. Use HashMaps keyed by package name for O(n) set operations instead of nested loops.
- Use shared query helpers from `common/src/db/query.rs` for any database filtering.
- All errors must return `Result<T, AppError>` using `.context()` wrapping per `common/src/error.rs` pattern.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service for fetching SBOM data; use its methods rather than writing raw queries
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Existing service for fetching package data
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Existing service for fetching advisory data
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — Standard error type with IntoResponse implementation
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying package associations
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for querying advisory associations
- `entity/src/package_license.rs` — Package-License mapping entity for license comparison

## Acceptance Criteria
- [ ] `SbomComparisonService::compare()` correctly computes all six diff categories
- [ ] Returns 404 AppError when either SBOM ID does not exist
- [ ] Handles the case where both SBOMs are identical (all diff categories empty)
- [ ] Handles the case where SBOMs share no packages (all packages are added/removed)
- [ ] Performance: completes within 1s for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Unit test: compare two SBOMs with known differences — verify added, removed, version-changed packages
- [ ] Unit test: compare two SBOMs with vulnerability differences — verify new and resolved vulnerabilities
- [ ] Unit test: compare two SBOMs with license changes — verify license change detection
- [ ] Unit test: compare identical SBOMs — verify all diff categories are empty
- [ ] Unit test: compare with non-existent SBOM ID — verify 404 error response
- [ ] Unit test: verify upgrade/downgrade direction detection in version changes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison diff model structs
