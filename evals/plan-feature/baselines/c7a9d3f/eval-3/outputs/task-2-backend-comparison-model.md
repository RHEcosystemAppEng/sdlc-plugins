## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add model types for the SBOM comparison result. These types define the structured diff response shape returned by the comparison endpoint, including added/removed packages, version changes, new/resolved vulnerabilities, and license changes.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison result structs: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new module

## API Changes
- Response shape for the comparison endpoint (consumed by Task 3):
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/`: each model struct uses `#[derive(Clone, Debug, Serialize, Deserialize)]` and is defined in its own file within the `model/` directory. See `summary.rs` and `details.rs` for examples.
- The `SbomComparisonResult` struct should contain six Vec fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`.
- `PackageDiff` struct: `name: String`, `version: String`, `license: Option<String>`, `advisory_count: u32` — used for both added and removed packages.
- `VersionChange` struct: `name: String`, `left_version: String`, `right_version: String`, `direction: String` (values: "upgrade" or "downgrade").
- `VulnerabilityDiff` struct: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String` (or `previously_affected_package` for resolved).
- `LicenseChange` struct: `name: String`, `left_license: String`, `right_license: String`.
- Derive `Serialize` for all structs so they can be returned as JSON from the Axum handler.
- All handlers return `Result<T, AppError>` with `.context()` wrapping per the backend conventions in `common/src/error.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference for struct patterns with Serialize/Deserialize derives
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — Reference for more complex model types
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains severity field pattern that `VulnerabilityDiff` should mirror
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Contains license field pattern that `PackageDiff` should mirror

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category fields
- [ ] `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` structs are defined with correct fields
- [ ] All structs derive `Serialize` and `Deserialize`
- [ ] Module is exported from `model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Verify structs can be serialized to JSON matching the expected response shape
- [ ] Verify deserialization round-trip for each struct

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
