## Repository
trustify-backend

## Target Branch
main

## Description
Define the Rust model types for the SBOM comparison result. These structs represent the structured diff returned by the comparison endpoint, covering added/removed packages, version changes, new/resolved vulnerabilities, and license changes. Establishing these types first allows the service and endpoint layers to be built on a stable contract.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Structs for the comparison response: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to export the new module

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs`. Each struct should derive `Serialize`, `Deserialize`, `Clone`, and `Debug`. The `SbomComparisonResult` struct should contain six fields matching the API response shape: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`. The `VulnerabilityDiff` struct should include a `severity` field typed as a string (matching `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`). The `VersionChange` struct should include a `direction` enum field with values `Upgrade` and `Downgrade`.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference for struct conventions and serde derivations
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference for severity field typing

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct exists with all six diff category fields
- [ ] `PackageDiff` struct has fields: name, version, license, advisory_count
- [ ] `VersionChange` struct has fields: name, left_version, right_version, direction
- [ ] `VulnerabilityDiff` struct has fields: advisory_id, severity, title, affected_package
- [ ] `LicenseChange` struct has fields: name, left_license, right_license
- [ ] All structs derive Serialize, Deserialize, Clone, Debug
- [ ] Module is exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test verifying `SbomComparisonResult` serializes to the expected JSON shape
- [ ] Unit test verifying `VersionChange` direction field serializes as lowercase ("upgrade"/"downgrade")

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental -- comparison` — model tests pass
