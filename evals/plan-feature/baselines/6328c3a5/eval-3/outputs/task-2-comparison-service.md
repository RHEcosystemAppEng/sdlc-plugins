## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the SBOM comparison model types and service logic that computes a structured diff between two SBOMs. The service fetches package lists and advisory associations for both SBOMs, then computes: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. This is the core diffing engine consumed by the comparison REST endpoint (Task 3).

Per the non-functional requirements, the diff must be computed on-the-fly from existing package and advisory data without creating new database tables.

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` — Comparison result types: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomComparisonService` with `compare(left_id: Uuid, right_id: Uuid) -> Result<SbomComparisonResult, AppError>` method

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Export the `compare` module
- `modules/fundamental/src/sbom/service/mod.rs` — Export the `compare` service module
- `modules/fundamental/src/sbom/mod.rs` — Ensure model and service sub-modules are re-exported

## Implementation Notes
Per CONVENTIONS.md §Module Pattern: follow the established `model/ + service/ + endpoints/` structure. This task covers model and service; the endpoint is created in Task 3.
Applies: task creates `modules/fundamental/src/sbom/model/compare.rs` matching the convention's module directory scope.

Per CONVENTIONS.md §Error Handling: all service methods must return `Result<T, AppError>` and use `.context()` for error wrapping.
Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` file scope.

**Diff algorithm outline:**
1. Fetch package lists for both SBOMs via `PackageService` (using `sbom_package` join table)
2. Index packages by name to identify added (right-only), removed (left-only), and common packages
3. For common packages: compare versions to detect upgrades/downgrades
4. For common packages: compare `package_license` entries to detect license changes
5. Fetch advisories for both SBOMs via `AdvisoryService` (using `sbom_advisory` join table)
6. Diff advisory sets to identify new and resolved vulnerabilities
7. Populate `SbomComparisonResult` with all diff categories

**Performance:** p95 < 1s for SBOMs with up to 2000 packages. Use HashMaps for O(n) comparison instead of nested loops.

**Response shape** (matches Figma design contract):
```rust
pub struct SbomComparisonResult {
    pub added_packages: Vec<AddedPackage>,
    pub removed_packages: Vec<RemovedPackage>,
    pub version_changes: Vec<VersionChange>,
    pub new_vulnerabilities: Vec<NewVulnerability>,
    pub resolved_vulnerabilities: Vec<ResolvedVulnerability>,
    pub license_changes: Vec<LicenseChange>,
}
```

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — fetches SBOM details; use to validate both SBOM IDs exist before computing diff
- `modules/fundamental/src/package/service/mod.rs::PackageService` — fetches packages; use to retrieve package lists for each SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — fetches advisories; use to retrieve advisory associations for each SBOM
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM summary struct; reference for field naming conventions
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — includes severity field; use for vulnerability severity in diff results
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — includes license field; use for license comparison
- `common/src/error.rs::AppError` — standard error type for all service methods

## Acceptance Criteria
- [ ] `SbomComparisonResult` and all sub-types are defined with `Serialize`/`Deserialize` derives
- [ ] `SbomComparisonService::compare()` correctly identifies added packages (present in right SBOM only)
- [ ] `SbomComparisonService::compare()` correctly identifies removed packages (present in left SBOM only)
- [ ] `SbomComparisonService::compare()` correctly identifies version changes with upgrade/downgrade direction
- [ ] `SbomComparisonService::compare()` correctly identifies new vulnerabilities (advisories affecting right SBOM only)
- [ ] `SbomComparisonService::compare()` correctly identifies resolved vulnerabilities (advisories affecting left SBOM only)
- [ ] `SbomComparisonService::compare()` correctly identifies license changes for common packages
- [ ] Service returns `AppError` (404) when either SBOM ID does not exist

## Test Requirements
- [ ] Unit test: comparison of two SBOMs with added, removed, and unchanged packages
- [ ] Unit test: comparison detecting version upgrades and downgrades
- [ ] Unit test: comparison detecting new and resolved vulnerabilities with correct severity
- [ ] Unit test: comparison detecting license changes
- [ ] Unit test: comparison with empty package lists (both SBOMs have no packages)
- [ ] Unit test: error handling when SBOM ID does not exist
- [ ] Performance consideration: test with large package lists to verify O(n) behavior

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
