## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the Rust data model structs for the SBOM comparison response. These structs represent the structured diff between two SBOMs: added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The models follow the existing pattern in `modules/fundamental/src/sbom/model/` and will be serialized as the JSON response for the comparison endpoint.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison response structs: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs`. Each struct should derive `Serialize, Deserialize, Debug, Clone, PartialEq`.

The `SbomComparison` struct should contain:
- `added_packages: Vec<PackageDiff>` — packages in right SBOM but not left
- `removed_packages: Vec<PackageDiff>` — packages in left SBOM but not right
- `version_changes: Vec<VersionChange>` — packages with differing versions
- `new_vulnerabilities: Vec<VulnerabilityDiff>` — advisories affecting right but not left
- `resolved_vulnerabilities: Vec<VulnerabilityDiff>` — advisories affecting left but not right
- `license_changes: Vec<LicenseChange>` — packages with differing licenses

`PackageDiff` fields: `name: String`, `version: String`, `license: Option<String>`, `advisory_count: u32`.

`VersionChange` fields: `name: String`, `left_version: String`, `right_version: String`, `direction: String` (upgrade/downgrade).

`VulnerabilityDiff` fields: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`.

`LicenseChange` fields: `name: String`, `left_license: String`, `right_license: String`.

Per CONVENTIONS.md §Module pattern: place model structs under `model/` within the sbom module directory.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's `model/` directory scope.

Per CONVENTIONS.md §Framework: use SeaORM-compatible derive macros and Serde for serialization.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct patterns and derive macros
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — reference for nested response structures
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for severity field pattern
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reference for license field pattern

## Acceptance Criteria
- [ ] `SbomComparison` struct defined with all six diff category fields
- [ ] `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` structs defined with correct fields
- [ ] All structs derive `Serialize, Deserialize, Debug, Clone, PartialEq`
- [ ] Module is exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors: `cargo check -p trustify-module-fundamental`

## Test Requirements
- [ ] Verify `SbomComparison` serializes to the expected JSON shape matching the API contract
- [ ] Verify deserialization round-trip for each struct

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental -- comparison` — model tests pass

## Dependencies
- Depends on: Task 1 — create-branch

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:3bd1d677c3055727d741bb1cb36a30b25c2fe6d8b43dbd68bca1712267b2ed10
