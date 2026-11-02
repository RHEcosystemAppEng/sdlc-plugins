## Repository
trustify-backend

## Target Branch
main

## Description
Create the `SbomComparisonResult` response model and its constituent types for the SBOM comparison feature (TC-9003). This model represents the structured diff between two SBOMs, including sections for added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — defines `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` structs with Serialize derives

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod comparison;` to export the new module

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/`:
- `summary.rs` defines `SbomSummary` with `#[derive(Serialize, Deserialize, Debug)]` — use the same derive pattern for `SbomComparisonResult`
- `details.rs` defines `SbomDetails` — follow the same struct documentation style
- Each section type (`AddedPackage`, `RemovedPackage`, etc.) should be a flat struct with fields matching the expected API response shape from the Figma design context:
  - `AddedPackage`: `name: String`, `version: String`, `license: String`, `advisory_count: i64`
  - `RemovedPackage`: same fields as `AddedPackage`
  - `VersionChange`: `name: String`, `left_version: String`, `right_version: String`, `direction: String`
  - `NewVulnerability`: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`
  - `ResolvedVulnerability`: `advisory_id: String`, `severity: String`, `title: String`, `previously_affected_package: String`
  - `LicenseChange`: `name: String`, `left_license: String`, `right_license: String`
- `SbomComparisonResult`: `added_packages: Vec<AddedPackage>`, `removed_packages: Vec<RemovedPackage>`, `version_changes: Vec<VersionChange>`, `new_vulnerabilities: Vec<NewVulnerability>`, `resolved_vulnerabilities: Vec<ResolvedVulnerability>`, `license_changes: Vec<LicenseChange>`

Per CONVENTIONS.md §Module pattern: each domain follows model/ + service/ + endpoints/ structure.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's model module scope.

Per CONVENTIONS.md §Error handling: all public types use `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's Rust module scope.

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff section fields
- [ ] All constituent types (`AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) are defined with correct fields
- [ ] All structs derive `Serialize` for JSON response serialization
- [ ] Module is exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Verify `SbomComparisonResult` can be serialized to JSON matching the expected response shape
- [ ] Verify each constituent type serializes field names in snake_case (matching the API contract)

## Dependencies
- None
