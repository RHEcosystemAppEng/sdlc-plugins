## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the data model and service logic for SBOM comparison. This introduces the `SbomComparisonResult` response struct with its sub-structs for each diff category (added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes), and a comparison method on `SbomService` that computes the structured diff between two SBOMs by querying their associated packages, advisories, and licenses.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — SbomComparisonResult struct and sub-structs (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod comparison;` to expose the new model module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare_sboms(left_id, right_id)` method to SbomService

## Implementation Notes
- Follow the existing model pattern: each domain entity has its own file under `model/` (see `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for examples).
- The `SbomComparisonResult` struct must derive `Serialize` and `Deserialize` to support JSON serialization via Axum.
- The comparison service method should:
  1. Fetch packages for both SBOMs using existing `PackageService` (see `modules/fundamental/src/package/service/mod.rs`)
  2. Compute set differences for added/removed packages by comparing package names
  3. Detect version changes for packages present in both SBOMs
  4. Fetch advisories linked to each SBOM via `sbom_advisory` join table (see `entity/src/sbom_advisory.rs`) and compute new/resolved vulnerability diffs
  5. Compare license fields from `PackageSummary` (see `modules/fundamental/src/package/model/summary.rs` which includes the `license` field) to detect license changes
- Use `Result<T, AppError>` return type with `.context()` wrapping per the existing error handling pattern (see `common/src/error.rs`).
- Per the non-functional requirement: no new database tables. Compute the diff on-the-fly from existing package, advisory, and sbom_package/sbom_advisory join data.
- The `direction` field in `VersionChange` should be computed by comparing semver strings (upgrade vs downgrade).

**Reuse Candidates:**
- `modules/fundamental/src/package/service/mod.rs::PackageService` — use existing package fetching logic to retrieve packages for each SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — use existing advisory fetching/search to find advisories per SBOM
- `entity/src/sbom_package.rs` — existing SBOM-Package join table entity for querying packages belonging to an SBOM
- `entity/src/sbom_advisory.rs` — existing SBOM-Advisory join table entity for querying advisories affecting an SBOM
- `entity/src/package_license.rs` — existing Package-License mapping for license comparison
- `common/src/error.rs::AppError` — reuse the standard error type

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff categories matching the expected API response shape
- [ ] `SbomService::compare_sboms` method correctly computes added/removed packages, version changes, new/resolved vulnerabilities, and license changes
- [ ] Method returns `Result<SbomComparisonResult, AppError>`
- [ ] No new database tables or migrations are introduced

## Test Requirements
- [ ] Unit test: comparison of two SBOMs with known package differences produces correct added/removed sets
- [ ] Unit test: version change detection correctly identifies upgrades vs downgrades
- [ ] Unit test: vulnerability diff correctly identifies new and resolved advisories
- [ ] Unit test: license change detection works for packages with changed licenses
- [ ] Unit test: comparison of identical SBOMs returns empty diff categories

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
