# Task 2 — Add SBOM comparison diff model structs

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the data model structs for the SBOM comparison diff result. These structs represent the structured diff between two SBOMs, covering added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The comparison endpoint (Task 3) and service layer (Task 3) will use these types as the response shape.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison result structs: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each struct derives `Serialize`, `Deserialize`, `Clone`, `Debug` and uses `#[serde(rename_all = "snake_case")]`.
- The `SbomComparisonResult` struct should contain six fields matching the API response shape from the Figma design context:
  - `added_packages: Vec<AddedPackage>` — fields: `name`, `version`, `license`, `advisory_count`
  - `removed_packages: Vec<RemovedPackage>` — fields: `name`, `version`, `license`, `advisory_count`
  - `version_changes: Vec<VersionChange>` — fields: `name`, `left_version`, `right_version`, `direction` (enum: `upgrade`, `downgrade`)
  - `new_vulnerabilities: Vec<NewVulnerability>` — fields: `advisory_id`, `severity`, `title`, `affected_package`
  - `resolved_vulnerabilities: Vec<ResolvedVulnerability>` — fields: `advisory_id`, `severity`, `title`, `previously_affected_package`
  - `license_changes: Vec<LicenseChange>` — fields: `name`, `left_license`, `right_license`
- The `direction` field on `VersionChange` should be a string enum (`"upgrade"` / `"downgrade"`) — use a Rust enum with `#[serde(rename_all = "lowercase")]`.
- The `severity` field on vulnerability structs should be a string matching the existing severity representation used in `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`).

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM model struct, follow its derive macros and serialization conventions
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains `severity` field type/representation to reuse for vulnerability severity
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains `license` field type to align with

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category fields
- [ ] Each diff category has its own struct with the fields specified in the API response shape
- [ ] `VersionChange` includes a `direction` enum with `upgrade` and `downgrade` variants
- [ ] All structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`
- [ ] The module is exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test verifying `SbomComparisonResult` serializes to the expected JSON shape (matching the API contract in the Figma design context)
- [ ] Unit test verifying `VersionChange` direction enum serializes as lowercase strings

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
