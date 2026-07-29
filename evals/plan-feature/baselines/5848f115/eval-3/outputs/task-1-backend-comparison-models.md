## Repository
trustify-backend

## Target Branch
main

## Description
Add the model structs for the SBOM comparison diff result. These structs define the response shape for the new comparison endpoint, covering all six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Structs for SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct layout and derive macros.
- All structs must derive `Serialize` and `Deserialize` (serde) for JSON response serialization.
- The `SbomComparisonResult` struct contains six fields matching the API response shape from the feature specification:
  - `added_packages: Vec<AddedPackage>` — fields: name, version, license, advisory_count
  - `removed_packages: Vec<RemovedPackage>` — fields: name, version, license, advisory_count
  - `version_changes: Vec<VersionChange>` — fields: name, left_version, right_version, direction (enum: upgrade/downgrade)
  - `new_vulnerabilities: Vec<NewVulnerability>` — fields: advisory_id, severity, title, affected_package
  - `resolved_vulnerabilities: Vec<ResolvedVulnerability>` — fields: advisory_id, severity, title, previously_affected_package
  - `license_changes: Vec<LicenseChange>` — fields: name, left_license, right_license
- The `direction` field in VersionChange should be a `String` or an enum serialized as lowercase (e.g., "upgrade", "downgrade").
- Reference the `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` for field naming conventions (it includes `license` field).
- Reference the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` for severity field representation.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — demonstrates the model struct pattern with serde derives used in this module
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — shows field naming for package name, version, and license
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — shows severity field representation

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct exists with all six category fields
- [ ] All sub-structs (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) are defined with correct fields
- [ ] All structs derive Serialize and Deserialize
- [ ] The module is exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] The response shape matches the API contract specified in the feature description

## Test Requirements
- [ ] Verify that SbomComparisonResult serializes to the expected JSON shape with all six sections
- [ ] Verify that an empty SbomComparisonResult (all empty vectors) serializes correctly
- [ ] Verify that VersionChange direction field serializes as lowercase string

## Verification Commands
- `cargo build -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental` — all existing tests pass

## Dependencies
- None (this is the first task)
