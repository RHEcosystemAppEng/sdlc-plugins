## Repository
trustify-backend

## Target Branch
main

## Description
Add the data model types and service logic for SBOM comparison. This creates the structured diff representation (added/removed packages, version changes, new/resolved vulnerabilities, license changes) and the service method that computes the diff between two SBOMs by querying existing package, advisory, and license data. No new database tables are needed -- the diff is computed on-the-fly from existing entities.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` -- Comparison result types: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `modules/fundamental/src/sbom/service/compare.rs` -- `SbomService::compare()` method that loads packages, advisories, and licenses for both SBOMs and computes the structured diff

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod comparison;` re-export
- `modules/fundamental/src/sbom/service/mod.rs` -- Add `pub mod compare;` re-export

## Implementation Notes
- Follow the existing module pattern: `model/` for data types, `service/` for business logic. See `modules/fundamental/src/sbom/model/summary.rs` for the established model struct pattern and `modules/fundamental/src/sbom/service/sbom.rs` for the service method pattern.
- All model types must derive `Serialize`, `Deserialize`, `Debug`, and `Clone` to match existing model conventions (see `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs`).
- The `SbomComparisonResult` struct must match the API response shape from the design specification:
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
- `PackageDiff` fields: `name: String`, `version: String`, `license: String`, `advisory_count: i64` (matching the Added/Removed Packages table columns in the UI design).
- `VersionChange` fields: `name: String`, `left_version: String`, `right_version: String`, `direction: ChangeDirection` where `ChangeDirection` is an enum with `Upgrade` and `Downgrade` variants.
- `VulnerabilityDiff` fields: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`. Use a single struct covering both new and resolved vulnerabilities -- the `affected_package` field represents `affected_package` for new and `previously_affected_package` for resolved.
- `LicenseChange` fields: `name: String`, `left_license: String`, `right_license: String`.
- The comparison service must compute the diff on-the-fly from existing data (no new database tables per NFR). Use existing `PackageService` to fetch packages for each SBOM via the `sbom_package` join table (`entity/src/sbom_package.rs`), `AdvisoryService` to fetch advisories via the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`), and the `package_license` entity (`entity/src/package_license.rs`) for license data.
- Use `PackageSummary.license` field (from `modules/fundamental/src/package/model/summary.rs`) for license comparison and `AdvisorySummary.severity` field (from `modules/fundamental/src/advisory/model/summary.rs`) for vulnerability severity.
- Compute version direction by comparing semver strings: if left < right then `Upgrade`, if left > right then `Downgrade`. Consider using the `semver` crate if available, or fall back to string comparison.
- Error handling: return `Result<SbomComparisonResult, AppError>` with `.context()` wrapping per the established error handling pattern (see `common/src/error.rs`).
- Per CONVENTIONS.md section Module pattern: follow model/ + service/ + endpoints/ structure.
  Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's `.rs` module scope.
- Per CONVENTIONS.md section Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` service scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- Existing service with methods to fetch SBOM details and list SBOMs; extend with a `compare()` method for comparison logic
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- Fetch packages linked to an SBOM; reuse for retrieving package lists to diff
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- Fetch advisories linked to an SBOM; reuse for vulnerability diff computation
- `entity/src/sbom_package.rs` -- SBOM-Package join entity; use to query packages per SBOM
- `entity/src/sbom_advisory.rs` -- SBOM-Advisory join entity; use to query advisories per SBOM
- `entity/src/package_license.rs` -- Package-License mapping entity; use for license change detection
- `common/src/model/paginated.rs::PaginatedResults` -- Reference for response struct patterns and derives

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct and all sub-types (`PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`, `ChangeDirection`) are defined with `Serialize`/`Deserialize`/`Debug`/`Clone` derives
- [ ] `SbomService::compare(left_id, right_id)` method computes the correct diff across all six categories
- [ ] Added packages are those in right SBOM but not in left (by package name)
- [ ] Removed packages are those in left SBOM but not in right (by package name)
- [ ] Version changes detect packages present in both SBOMs with different versions, including correct upgrade/downgrade direction
- [ ] New vulnerabilities are advisories affecting right SBOM but not left
- [ ] Resolved vulnerabilities are advisories affecting left SBOM but not right
- [ ] License changes detect packages present in both SBOMs with different license values
- [ ] All service errors are wrapped with `.context()` and return `AppError`

## Test Requirements
- [ ] Unit test: comparison of two SBOMs with known package sets produces correct added/removed/changed lists
- [ ] Unit test: version change direction correctly classifies upgrades vs downgrades (semver comparison)
- [ ] Unit test: comparison of identical SBOMs returns empty diff across all six categories
- [ ] Unit test: comparison handles SBOMs with no overlapping packages (all added on one side, all removed on the other)
- [ ] Unit test: vulnerability diff correctly identifies new and resolved advisories

## Dependencies
- None (first task in the feature)

---
sha256-md:30a25fd19d81b9dd0ad7d8954dee0b9e4333fa8d20f8ce9d8528c9579ac816c0
