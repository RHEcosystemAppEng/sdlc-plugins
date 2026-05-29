# Task 1 — Add SBOM comparison model structs

## Repository
trustify-backend

## Target Branch
main

## Description
Add model structs for the SBOM comparison diff response. These structs represent the result of comparing two SBOMs: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. The models will be used by the comparison service (Task 2) and serialized as JSON by the comparison endpoint (Task 3).

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison result structs: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` JSON (this task defines the response types; the endpoint itself is Task 3)

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each struct derives `Serialize`, `Deserialize`, `Debug`, `Clone` and uses serde attributes for JSON field naming.
- The response shape must match the contract specified in the feature:
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
- Use `#[serde(rename_all = "snake_case")]` on structs to ensure JSON field names use snake_case.
- The `direction` field in `VersionChange` should be an enum with variants `Upgrade` and `Downgrade`, serialized as lowercase strings.
- The `severity` field in vulnerability structs should reuse or align with the severity representation from `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Follow struct patterns (derive macros, serde configuration)
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reuse or align the severity field type
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Reference for package name/version/license field types

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct with all six diff category fields is defined and compiles
- [ ] Each diff category uses a dedicated struct with the fields specified in the API contract
- [ ] `VersionChange.direction` is an enum serializing to `"upgrade"` or `"downgrade"`
- [ ] All structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- [ ] The model module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Add unit tests in `comparison.rs` verifying that `SbomComparisonResult` serializes to the expected JSON shape
- [ ] Test that `VersionChange` direction enum serializes as lowercase strings

## Verification Commands
- `cargo build -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental comparison` — model serialization tests pass

## Dependencies
- None
