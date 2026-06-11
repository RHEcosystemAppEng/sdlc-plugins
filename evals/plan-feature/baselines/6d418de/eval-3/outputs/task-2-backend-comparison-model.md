# Task 2 — Add SBOM comparison model structs

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the Rust data model structs for the SBOM comparison result. These structs represent the structured diff between two SBOMs, covering added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The structs will be used by the comparison service and serialized as the endpoint response.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison result structs: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new module

## API Changes
- Response shape for `GET /api/v2/sbom/compare` — NEW: defines the `SbomComparisonResult` struct with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs` — derive `Serialize`, `Deserialize`, `Debug`, `Clone` on all structs, use `#[serde(rename_all = "snake_case")]`.
- `PackageDiff` struct fields: `name: String`, `version: String`, `license: Option<String>`, `advisory_count: u64`. Used for both `added_packages` and `removed_packages`.
- `VersionChange` struct fields: `name: String`, `left_version: String`, `right_version: String`, `direction: VersionDirection`. Define `VersionDirection` as an enum with variants `Upgrade` and `Downgrade`.
- `VulnerabilityDiff` struct fields: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`. Used for both `new_vulnerabilities` and `resolved_vulnerabilities` (the `affected_package` field serves as `previously_affected_package` contextually).
- `LicenseChange` struct fields: `name: String`, `left_license: String`, `right_license: String`.
- `SbomComparisonResult` struct fields: `added_packages: Vec<PackageDiff>`, `removed_packages: Vec<PackageDiff>`, `version_changes: Vec<VersionChange>`, `new_vulnerabilities: Vec<VulnerabilityDiff>`, `resolved_vulnerabilities: Vec<VulnerabilityDiff>`, `license_changes: Vec<LicenseChange>`.
- No new database tables needed — these are pure computation result structs, not SeaORM entities.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for the struct derivation pattern and serde configuration
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for severity field representation
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reference for package/license field naming

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category fields
- [ ] `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` structs are defined with correct fields
- [ ] `VersionDirection` enum has `Upgrade` and `Downgrade` variants
- [ ] All structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- [ ] Module is publicly exported from `model/mod.rs`

## Test Requirements
- [ ] Verify structs serialize to the expected JSON shape matching the API contract (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] Verify `VersionDirection` serializes as lowercase snake_case strings ("upgrade", "downgrade")

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
