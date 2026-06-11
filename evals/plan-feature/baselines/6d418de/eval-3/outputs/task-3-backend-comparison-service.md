# Task 3 — Add SBOM comparison service logic

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the comparison service logic that computes a structured diff between two SBOMs. The service fetches package lists, advisory associations, and license data for both SBOMs, then computes the six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. All computation is done on-the-fly from existing data — no new database tables.

## Files to Create
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomComparisonService` with a `compare(db: &DbConn, left_id: Uuid, right_id: Uuid) -> Result<SbomComparisonResult, AppError>` method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to expose the new module

## Implementation Notes
- Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs` — accept a `&DbConn` parameter, return `Result<T, AppError>` with `.context()` error wrapping.
- Use SeaORM entity queries on existing entities: `entity/src/sbom.rs`, `entity/src/sbom_package.rs`, `entity/src/package.rs`, `entity/src/sbom_advisory.rs`, `entity/src/advisory.rs`, `entity/src/package_license.rs`.
- **Algorithm outline:**
  1. Validate both SBOM IDs exist; return 404 `AppError` if either is missing.
  2. Fetch all packages for left SBOM via `sbom_package` join to `package` entity.
  3. Fetch all packages for right SBOM via the same join.
  4. Compute set differences using package name as the key:
     - Added: in right but not in left
     - Removed: in left but not in right
     - Version changes: in both but with different versions; determine direction by comparing version strings (use semver parsing if available, otherwise lexicographic)
  5. For each package, count associated advisories via `sbom_advisory` join.
  6. Fetch advisories for left and right SBOMs via `sbom_advisory` entity. Compute new vulnerabilities (in right but not left) and resolved vulnerabilities (in left but not right) using advisory ID as the key. Include severity from `AdvisorySummary`.
  7. Compare licenses for packages present in both SBOMs via `package_license` entity. Detect changes where the license string differs.
- **Performance:** The non-functional requirement specifies p95 < 1s for SBOMs with up to 2000 packages each. Use batch queries (fetch all packages for an SBOM in one query) rather than per-package queries. Consider using `HashSet` for O(1) lookups during set difference computation.
- Use `common/src/error.rs::AppError` for error handling, consistent with other services.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference for the service struct pattern, database connection handling, and error wrapping
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference for querying advisory data and extracting severity
- `modules/fundamental/src/package/service/mod.rs::PackageService` — reference for querying package data
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `compare` method accepts two SBOM IDs and returns `SbomComparisonResult`
- [ ] Returns 404 error if either SBOM ID does not exist
- [ ] Correctly computes added packages (in right, not in left)
- [ ] Correctly computes removed packages (in left, not in right)
- [ ] Correctly computes version changes with upgrade/downgrade direction
- [ ] Correctly computes new vulnerabilities (advisories in right SBOM, not in left)
- [ ] Correctly computes resolved vulnerabilities (advisories in left SBOM, not in right)
- [ ] Correctly computes license changes for packages present in both SBOMs
- [ ] Advisory count is populated for each package in added/removed lists
- [ ] All diff computations use batch queries for performance

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package differences, verify added/removed/changed lists
- [ ] Unit test: compare two identical SBOMs, verify all diff lists are empty
- [ ] Unit test: compare with non-existent SBOM ID returns 404 error
- [ ] Unit test: verify version direction detection (upgrade when right version > left, downgrade when right version < left)
- [ ] Unit test: verify vulnerability diff includes correct severity and affected package
- [ ] Unit test: verify license change detection when a package's license changes between SBOMs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model structs
