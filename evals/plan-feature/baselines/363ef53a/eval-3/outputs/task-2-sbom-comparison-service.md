## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison diff model and service logic that computes structured differences between two SBOMs. The service fetches package lists, advisory associations, and license mappings for both SBOMs, then produces a diff result containing added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. This is the core business logic consumed by the comparison REST endpoint (Task 3).

The diff must be computed on-the-fly from existing package and advisory data — no new database tables are required (per non-functional requirements).

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison diff model structs: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomService::compare()` method: fetches both SBOMs' package sets, computes set differences, correlates advisories, detects license changes

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Register the `comparison` submodule and re-export comparison types
- `modules/fundamental/src/sbom/service/mod.rs` — Register the `compare` submodule

## Implementation Notes
Follow the existing module pattern in `modules/fundamental/src/sbom/`: the model structs go in `model/` and the service logic goes in `service/`. Each struct should derive `Serialize`, `Deserialize`, `Clone`, `Debug` as seen in the existing `SbomSummary` (in `model/summary.rs`) and `SbomDetails` (in `model/details.rs`).

Per the repo's module pattern convention: each domain module follows `model/ + service/ + endpoints/` structure.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's Rust module file scope (`.rs` files under `modules/`).

Per the repo's error handling convention: all service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's Rust service file scope.

**Diff computation approach:**
1. Use `SbomService::fetch()` (in `service/sbom.rs`) to load both SBOMs
2. Use `PackageService::list()` (in `package/service/mod.rs`) to get package lists for each SBOM, keyed by package name
3. Set-difference the package name keys to find added/removed packages
4. For packages in both sets, compare versions to find version changes (direction = upgrade if right > left)
5. Query `AdvisoryService` (in `advisory/service/advisory.rs`) for advisories linked to each SBOM via `sbom_advisory` join table, then set-difference to find new/resolved vulnerabilities
6. Compare `PackageSummary.license` field for packages in both sets to find license changes

**Response shape** (matching Figma design backend interactions):
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

**Performance:** The comparison must complete within p95 < 1s for SBOMs with up to 2000 packages each. Use batch queries rather than N+1 fetches — load all packages and advisories for each SBOM in two queries, then compute the diff in memory.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods for loading SBOM data
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing service for loading package lists by SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing service for loading advisories
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing model struct to reference for serialization pattern
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing model struct with `license` field used in license change detection
- `common/src/error.rs::AppError` — shared error type for Result return types

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct and all sub-structs are defined with Serialize/Deserialize derives
- [ ] `SbomService::compare(left_id, right_id)` computes correct diffs for added, removed, changed packages
- [ ] New vulnerabilities are correctly identified (advisories in right SBOM not in left)
- [ ] Resolved vulnerabilities are correctly identified (advisories in left SBOM not in right)
- [ ] License changes are detected for packages present in both SBOMs
- [ ] Version change direction is correctly classified as "upgrade" or "downgrade"
- [ ] Service returns `AppError` with appropriate context for invalid SBOM IDs

## Test Requirements
- [ ] Unit test: compare two SBOMs where right has added packages not in left
- [ ] Unit test: compare two SBOMs where left has packages not in right (removed)
- [ ] Unit test: compare two SBOMs with overlapping packages at different versions
- [ ] Unit test: compare two SBOMs with different advisory sets (new/resolved vulnerabilities)
- [ ] Unit test: compare two SBOMs with license changes on shared packages
- [ ] Unit test: compare identical SBOMs produces empty diff
- [ ] Unit test: invalid SBOM ID returns appropriate error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
