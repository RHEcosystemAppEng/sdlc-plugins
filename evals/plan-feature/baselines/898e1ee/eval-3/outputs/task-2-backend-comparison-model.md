## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the Rust model structs for the SBOM comparison response. These structs represent the structured diff returned by the comparison endpoint, covering added/removed packages, version changes, new/resolved vulnerabilities, and license changes.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Structs for the comparison response: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new module

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparison` (this task defines the response type; the endpoint is wired in a later task)

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/`. The `SbomDetails` struct in `modules/fundamental/src/sbom/model/details.rs` and `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` demonstrate the serialization and documentation conventions.

Define these structs with `Serialize` and `Deserialize` derives:

- `SbomComparison` — top-level response with fields: `added_packages: Vec<PackageDiff>`, `removed_packages: Vec<PackageDiff>`, `version_changes: Vec<VersionChange>`, `new_vulnerabilities: Vec<VulnerabilityDiff>`, `resolved_vulnerabilities: Vec<VulnerabilityDiff>`, `license_changes: Vec<LicenseChange>`
- `PackageDiff` — fields: `name: String`, `version: String`, `license: Option<String>`, `advisory_count: u32`
- `VersionChange` — fields: `name: String`, `left_version: String`, `right_version: String`, `direction: VersionDirection`
- `VersionDirection` — enum with variants `Upgrade`, `Downgrade`
- `VulnerabilityDiff` — fields: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`
- `LicenseChange` — fields: `name: String`, `left_license: String`, `right_license: String`

Reuse the severity field conventions from `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — pattern for struct definition with Serialize/Deserialize
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity field representation
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — license field representation

## Acceptance Criteria
- [ ] `SbomComparison` struct and all child types are defined in `modules/fundamental/src/sbom/model/comparison.rs`
- [ ] All structs derive `Serialize` and `Deserialize`
- [ ] Module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without warnings

## Test Requirements
- [ ] Unit test that `SbomComparison` serializes to the expected JSON shape matching the API contract from the feature specification
- [ ] Unit test that `VersionDirection` serializes as lowercase strings ("upgrade", "downgrade")

## Verification Commands
- `cargo build -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental comparison` — model tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch

[sdlc-workflow] Description digest: sha256-md:d1a2e346dad86857aeffeee573a2266fc1875b54a873c023575f6df15d672dd8
