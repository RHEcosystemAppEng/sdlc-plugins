## Repository
trustify-backend

## Target Branch
main

## Description
Create the SBOM comparison response model and diff service logic for feature TC-9003 (SBOM comparison view). This task introduces the data structures that represent a structured diff between two SBOMs (added/removed packages, version changes, new/resolved vulnerabilities, license changes) and the service layer that computes the diff on-the-fly from existing package and advisory data without requiring new database tables.

**Priority**: Critical (inherited from TC-9003)
**Fix Version**: RHTPA 1.5.0 (inherited from TC-9003)

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` — response model structs: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomCompareService` with `compare(left_id, right_id)` method that fetches packages and advisories for both SBOMs and computes the structured diff

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod compare;` to expose the new comparison model
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod compare;` to expose the new comparison service

## API Changes
- No public API changes in this task (service layer only; endpoint is Task 2)

## Implementation Notes
Follow the existing module pattern in `modules/fundamental/src/sbom/` where `model/` contains response structs and `service/` contains business logic.

The comparison response model should match the JSON shape expected by the frontend (from figma-context.md):
```rust
pub struct SbomComparisonResult {
    pub added_packages: Vec<PackageDiff>,
    pub removed_packages: Vec<PackageDiff>,
    pub version_changes: Vec<VersionChange>,
    pub new_vulnerabilities: Vec<VulnerabilityDiff>,
    pub resolved_vulnerabilities: Vec<VulnerabilityDiff>,
    pub license_changes: Vec<LicenseChange>,
}
```

The diff service should:
1. Use `SbomService` from `modules/fundamental/src/sbom/service/sbom.rs` to fetch SBOM details for both IDs
2. Use `PackageService` from `modules/fundamental/src/package/service/mod.rs` to fetch package lists for each SBOM
3. Use `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs` to fetch advisories linked to each SBOM
4. Compute set differences for packages (by package identifier), then enrich with version, license, and advisory data
5. Use shared query helpers from `common/src/db/query.rs` for any filtered data retrieval

The service method should return `Result<SbomComparisonResult, AppError>` using the error type from `common/src/error.rs` with `.context()` wrapping for any fallible operations.

Per CONVENTIONS.md §Framework: use SeaORM for database queries when fetching package and advisory data for the two SBOMs. Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's Rust scope.

Per CONVENTIONS.md §Module pattern: follow the model/ + service/ + endpoints/ structure for the comparison feature. Applies: convention has no file-type restriction (broadly applicable).

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping from the comparison service methods. Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's Rust syntax scope.

Per CONVENTIONS.md §Query helpers: use shared filtering and pagination utilities from `common/src/db/query.rs` when querying package and advisory data. Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's Rust scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service for fetching SBOM details; reuse to load both left and right SBOMs
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing service for fetching packages; reuse to load package lists per SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing service for fetching advisories; reuse to load advisory data for vulnerability diffing
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM summary struct; reuse for SBOM identity validation
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing package model with license field; reuse for package diff data
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing advisory model with severity field; reuse for vulnerability diff data
- `common/src/model/paginated.rs::PaginatedResults` — existing pagination wrapper; reuse if paginating large package lists internally
- `common/src/error.rs::AppError` — existing error type; reuse for all error returns

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with fields for added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, and license_changes
- [ ] Each diff category has its own typed struct (PackageDiff, VersionChange, VulnerabilityDiff, LicenseChange) with Serialize derived
- [ ] `compare(left_id, right_id)` service method correctly computes set differences between two SBOMs
- [ ] Diff computation works on-the-fly from existing data without creating new database tables
- [ ] Service returns appropriate errors for invalid SBOM IDs (not found)
- [ ] Version changes include direction indicator (upgrade/downgrade)

## Test Requirements
- [ ] Unit test: compare two SBOMs where the right has additional packages — verify added_packages is populated
- [ ] Unit test: compare two SBOMs where the right is missing packages — verify removed_packages is populated
- [ ] Unit test: compare two SBOMs with version differences — verify version_changes includes correct direction
- [ ] Unit test: compare identical SBOMs — verify all diff categories are empty
- [ ] Unit test: compare with invalid SBOM ID — verify AppError is returned

## Dependencies
- None (first task in the plan)
