## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Create the data model types and service logic for computing a structured diff between two SBOMs. The diff compares packages, vulnerability advisories, and licenses between a "left" and "right" SBOM, producing categorized results: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — SbomComparisonResult struct and sub-types (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- `modules/fundamental/src/sbom/service/compare.rs` — comparison service method that fetches both SBOMs' packages and advisories and computes the diff

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod comparison;` to expose the new model types
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod compare;` to expose the comparison service

## Implementation Notes
- Follow the existing module pattern: model types in `model/` and service logic in `service/`. See `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/service/sbom.rs` for the established pattern.
- Per CONVENTIONS.md §Module Pattern: use the `model/ + service/ + endpoints/` structure for the new comparison functionality.
  Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's Rust module file scope.
- Per CONVENTIONS.md §Error Handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping for error propagation.
  Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's Rust source file scope.
- The diff is computed on-the-fly from existing package and advisory data — no new database tables. Use `PackageService` and `AdvisoryService` to fetch the data for each SBOM.
- The `SbomComparisonResult` struct fields should match the expected API response shape:
  - `added_packages: Vec<PackageDiffEntry>` — packages in right but not left
  - `removed_packages: Vec<PackageDiffEntry>` — packages in left but not right
  - `version_changes: Vec<VersionChangeEntry>` — packages in both with different versions
  - `new_vulnerabilities: Vec<VulnerabilityDiffEntry>` — advisories affecting right but not left
  - `resolved_vulnerabilities: Vec<VulnerabilityDiffEntry>` — advisories affecting left but not right
  - `license_changes: Vec<LicenseChangeEntry>` — packages with different licenses
- Each entry type should implement `Serialize` for JSON response.
- Non-functional: comparison must handle SBOMs with up to 2000 packages each within p95 < 1s. Use hash-based lookups (HashMap) for package matching rather than nested iteration.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service for fetching SBOM data, use to load both SBOMs
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing service for fetching package data
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing service for fetching advisory data
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM model type for reference on struct patterns
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — includes license field, use as reference for package data shape
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — includes severity field, use for vulnerability entry shape

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct contains all six diff categories
- [ ] Comparison service method accepts two SBOM IDs and returns `Result<SbomComparisonResult, AppError>`
- [ ] Added/removed package detection correctly identifies packages unique to each SBOM
- [ ] Version change detection identifies packages present in both SBOMs with different versions, including direction (upgrade/downgrade)
- [ ] Vulnerability diff identifies advisories unique to each SBOM
- [ ] License change detection identifies packages with different licenses between the two SBOMs

## Test Requirements
- [ ] Unit tests for comparison logic with mock SBOM data covering all six diff categories
- [ ] Test edge cases: identical SBOMs (empty diff), completely disjoint SBOMs (all added/removed), SBOMs with >100 packages for performance validation

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
