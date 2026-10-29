## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the data model and service logic for computing a structured diff between two SBOMs. The comparison service takes two SBOM IDs, loads their package and advisory data from the existing database tables, and computes a diff across six categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. No new database tables are needed — the diff is computed on-the-fly from existing package, advisory, and license data.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — SbomComparison response struct and category sub-structs (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- `modules/fundamental/src/sbom/service/compare.rs` — SbomService::compare() method implementing the diff algorithm

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod comparison;` declaration
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod compare;` declaration

## Implementation Notes
Follow the existing module pattern in `modules/fundamental/src/sbom/`. Each domain area uses `model/` for data types and `service/` for business logic.

The comparison struct should be serializable with serde for JSON responses:

```rust
pub struct SbomComparison {
    pub added_packages: Vec<AddedPackage>,
    pub removed_packages: Vec<RemovedPackage>,
    pub version_changes: Vec<VersionChange>,
    pub new_vulnerabilities: Vec<NewVulnerability>,
    pub resolved_vulnerabilities: Vec<ResolvedVulnerability>,
    pub license_changes: Vec<LicenseChange>,
}
```

Use `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` for fetching SBOM details. Use `PackageService` in `modules/fundamental/src/package/service/mod.rs` for loading package data. Use `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` for loading advisory data.

Use the existing query helpers in `common/src/db/query.rs` for database queries. All errors must return `Result<T, AppError>` using `.context()` wrapping per the error handling convention in `common/src/error.rs`.

Performance constraint: p95 < 1s for SBOMs with up to 2000 packages each. Use set-based operations (HashSet intersections/differences) for the diff computation rather than nested loops.

Per CONVENTIONS.md: follow the existing `model/ + service/ + endpoints/` module structure for new domain logic.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's Rust module structure scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service for fetching SBOM data; reuse its fetch and list methods to load both SBOMs for comparison
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — existing SBOM detail struct; use as the basis for extracting package lists from each SBOM
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing package model with license field; reuse for package data in the diff
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing advisory model with severity field; reuse for vulnerability data in the diff
- `common/src/error.rs::AppError` — existing error type; use for all error handling in the comparison service

## Acceptance Criteria
- [ ] `SbomComparison` struct and all sub-structs are defined with serde serialization
- [ ] `SbomService::compare(left_id, right_id)` correctly computes added packages (in right but not left)
- [ ] `SbomService::compare(left_id, right_id)` correctly computes removed packages (in left but not right)
- [ ] `SbomService::compare(left_id, right_id)` correctly computes version changes (same package, different versions)
- [ ] `SbomService::compare(left_id, right_id)` correctly computes new vulnerabilities (advisories affecting right but not left)
- [ ] `SbomService::compare(left_id, right_id)` correctly computes resolved vulnerabilities (advisories affecting left but not right)
- [ ] `SbomService::compare(left_id, right_id)` correctly computes license changes (same package, different license)
- [ ] Service returns appropriate `AppError` when either SBOM ID does not exist
- [ ] Diff computation uses set-based operations for O(n) performance on SBOMs with up to 2000 packages

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package differences produces correct added/removed lists
- [ ] Unit test: compare two SBOMs with version changes produces correct version change entries with upgrade/downgrade direction
- [ ] Unit test: compare two SBOMs with different advisory associations produces correct new/resolved vulnerability lists
- [ ] Unit test: compare two SBOMs with license changes produces correct license change entries
- [ ] Unit test: compare an SBOM with itself returns empty diff in all categories
- [ ] Unit test: requesting comparison with a nonexistent SBOM ID returns an appropriate error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
