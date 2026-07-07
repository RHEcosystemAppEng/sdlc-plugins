# Task 1 -- SBOM comparison data model

## Repository
trustify-backend

## Target Branch
main

## Description
Define the data model struct for the SBOM comparison result. The SbomComparisonResult struct represents the structured diff between two SBOMs, including added/removed packages, version changes, new/resolved vulnerabilities, and license changes. These models will be used by the comparison service (Task 2) and serialized as JSON by the comparison endpoint (Task 3). No new database tables are needed -- these are computed structs, not entities.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` -- Comparison result structs: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod comparison;` to expose the new model module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) for struct definition conventions (derive macros, serde attributes, field naming).
- SbomComparisonResult contains six Vec fields: added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes.
- AddedPackage and RemovedPackage fields: name: String, version: String, license: String, advisory_count: usize.
- VersionChange fields: name: String, left_version: String, right_version: String, direction: String (values: "upgrade" or "downgrade").
- NewVulnerability and ResolvedVulnerability fields: advisory_id: String, severity: String, title: String, affected_package: String (or previously_affected_package for resolved).
- LicenseChange fields: name: String, left_license: String, right_license: String.
- All structs must derive Serialize, Deserialize, Clone, Debug and use `#[serde(rename_all = "snake_case")]` to match the API contract.
- Reference `modules/fundamental/src/advisory/model/summary.rs` (AdvisorySummary) for severity field patterns.
- Per CONVENTIONS.md Error Handling: no fallible operations in this module, but follow standard derive conventions. Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's `.rs` scope.

## Acceptance Criteria
- [ ] SbomComparisonResult struct is defined with all six diff category Vec fields
- [ ] All sub-structs (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) are defined with correct fields
- [ ] All structs derive Serialize/Deserialize and use snake_case field naming
- [ ] Module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] SbomComparisonResult can be serialized to JSON matching the expected API response shape

## Test Requirements
- [ ] Verify that SbomComparisonResult serializes to JSON with the expected field names
- [ ] Verify that an empty SbomComparisonResult (all empty Vecs) serializes correctly
