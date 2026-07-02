## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison result model types and implement the diff service logic that computes structured differences between two SBOMs. The service fetches both SBOMs by ID, compares their package lists, correlates advisory and license data, and returns a structured result with six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Register the new comparison module
- `modules/fundamental/src/sbom/service/mod.rs` — Register the new compare service module
- `modules/fundamental/Cargo.toml` — Add any needed dependencies for the comparison logic

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — SBOM comparison result types: SbomComparisonResult, PackageDiff, VersionChange, VulnerabilityDiff, LicenseChange
- `modules/fundamental/src/sbom/service/compare.rs` — SbomCompareService with compare(left_id, right_id) method that computes the structured diff

## Implementation Notes
- Follow the existing module pattern: model types in `model/` directory, business logic in `service/` directory. See `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/service/sbom.rs` for the established pattern.
- SbomComparisonResult struct should contain six Vec fields matching the Figma design's diff sections:
  - `added_packages: Vec<PackageDiff>` — packages in right SBOM but not in left
  - `removed_packages: Vec<PackageDiff>` — packages in left SBOM but not in right
  - `version_changes: Vec<VersionChange>` — packages in both with different versions
  - `new_vulnerabilities: Vec<VulnerabilityDiff>` — advisories affecting right but not left
  - `resolved_vulnerabilities: Vec<VulnerabilityDiff>` — advisories affecting left but not right
  - `license_changes: Vec<LicenseChange>` — packages whose license differs between versions
- All structs must derive `Serialize` for JSON response serialization.
- Error handling: return `Result<SbomComparisonResult, AppError>` with `.context()` wrapping on all fallible operations. See `common/src/error.rs` for the `AppError` enum.
- No new database tables — compute the diff on-the-fly by fetching package lists for each SBOM via existing `SbomService` and `PackageService`, then set-differencing them.
- Use `AdvisoryService` to correlate advisories with packages in each SBOM for vulnerability diff computation.
- Performance: the comparison must handle SBOMs with up to 2000 packages each within p95 < 1s. Use HashMap-based lookups for package comparison rather than nested iteration.

**Convention references:**
- Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` directory structure for the new comparison module.
  Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's Rust module scope.
- Per CONVENTIONS.md §Error handling: use `Result<T, AppError>` with `.context()` wrapping on all fallible operations.
  Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's Rust source scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — fetch SBOM by ID, list packages for an SBOM
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM summary type; PackageDiff fields mirror PackageSummary fields
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — query advisories by package to compute vulnerability diffs
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity field needed for VulnerabilityDiff
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — package name, version, license fields reusable for diff types
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper pattern (though comparison returns a single result, not paginated)

## Acceptance Criteria
- [ ] SbomComparisonResult and all sub-types are defined with Serialize derive
- [ ] SbomCompareService.compare(left_id, right_id) returns a correct structured diff for two SBOMs
- [ ] Added/removed package detection correctly identifies set differences
- [ ] Version change detection identifies packages present in both SBOMs with different versions
- [ ] Vulnerability diff correctly identifies advisories unique to each SBOM
- [ ] License change detection identifies packages whose license field differs
- [ ] Returns AppError::NotFound when either SBOM ID does not exist

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package differences, verify added/removed packages
- [ ] Unit test: compare two SBOMs with version changes, verify left_version and right_version and direction (upgrade/downgrade)
- [ ] Unit test: compare two SBOMs with different advisory correlations, verify new/resolved vulnerabilities
- [ ] Unit test: compare two SBOMs with license changes, verify left_license and right_license
- [ ] Unit test: compare identical SBOMs returns empty diff lists
- [ ] Unit test: non-existent SBOM ID returns AppError::NotFound

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main

[sdlc-workflow] Description digest: sha256-md:63ec73de87132f6042cad0eda4a0dcdae678f77a9a95bb40f4272fb71fab89d0
