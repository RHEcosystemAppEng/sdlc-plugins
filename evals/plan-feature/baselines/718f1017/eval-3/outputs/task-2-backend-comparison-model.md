## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the data model structs for the SBOM comparison result. These structs define the response shape for the comparison endpoint, covering all six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison result structs: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module

## API Changes
- Response shape for `GET /api/v2/sbom/compare` — NEW: defines `SbomComparisonResult` with fields: `added_packages: Vec<PackageDiff>`, `removed_packages: Vec<PackageDiff>`, `version_changes: Vec<VersionChange>`, `new_vulnerabilities: Vec<VulnerabilityDiff>`, `resolved_vulnerabilities: Vec<VulnerabilityDiff>`, `license_changes: Vec<LicenseChange>`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs` — each struct derives `Serialize, Deserialize, Clone, Debug` and uses serde rename attributes for snake_case JSON output.
- `PackageDiff` struct should include: `name: String`, `version: String`, `license: String`, `advisory_count: u32` — matching the Figma-specified table columns for Added/Removed Packages sections.
- `VersionChange` struct should include: `name: String`, `left_version: String`, `right_version: String`, `direction: String` (values: "upgrade" or "downgrade").
- `VulnerabilityDiff` struct should include: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String` — the `severity` field uses the same severity enum as `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`.
- `LicenseChange` struct should include: `name: String`, `left_license: String`, `right_license: String`.
- Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` structure for the sbom module.
  Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's Rust module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct derivations and serde patterns
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains severity field pattern to reuse for `VulnerabilityDiff`
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains license field pattern to reference for `PackageDiff`

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category fields
- [ ] All supporting structs (`PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`) are defined with correct field types
- [ ] All structs derive `Serialize, Deserialize, Clone, Debug`
- [ ] JSON field names use snake_case matching the Figma-specified response shape
- [ ] Module is exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Structs compile without errors
- [ ] Serialization roundtrip test: create `SbomComparisonResult` with sample data, serialize to JSON, verify field names match the expected API response shape

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main

<!-- [sdlc-workflow] Description digest: sha256-md:3cee5eafa9b6c24da656572dc23129aa45d8ebc2e3da6b27bbef313a4f1f07a2 -->
