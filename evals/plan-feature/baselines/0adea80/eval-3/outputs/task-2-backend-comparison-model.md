# Task 2 — Add SBOM comparison diff model structs

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the data model structs for the SBOM comparison result. These structs represent the structured diff between two SBOMs, including added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The models will be used by the comparison service (Task 3) and serialized as JSON by the comparison endpoint (Task 4).

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison result structs: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct definition conventions (derive macros, serde attributes, field naming).
- The `SbomComparisonResult` struct should contain six Vec fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`.
- `AddedPackage` and `RemovedPackage` fields: `name: String`, `version: String`, `license: String`, `advisory_count: usize`.
- `VersionChange` fields: `name: String`, `left_version: String`, `right_version: String`, `direction: String` (values: "upgrade" or "downgrade").
- `NewVulnerability` and `ResolvedVulnerability` fields: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String` (or `previously_affected_package` for resolved).
- `LicenseChange` fields: `name: String`, `left_license: String`, `right_license: String`.
- All structs must derive `Serialize`, `Deserialize`, `Clone`, `Debug` and use `#[serde(rename_all = "snake_case")]` to match the API contract.
- No new database tables — these are computed structs, not entities.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Example of model struct pattern with serde derives
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — Example of detailed model struct pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains severity field pattern to reference
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Contains license field pattern to reference

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category Vec fields
- [ ] All sub-structs (`AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) are defined with correct fields
- [ ] All structs derive Serialize/Deserialize and use snake_case field naming
- [ ] Module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Verify that `SbomComparisonResult` can be serialized to JSON matching the expected API response shape
- [ ] Verify that an empty `SbomComparisonResult` (all empty Vecs) serializes correctly

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
