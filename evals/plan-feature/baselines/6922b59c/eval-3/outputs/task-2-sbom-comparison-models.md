## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the model types for the SBOM comparison result. These types represent the structured diff between two SBOMs and serve as the response shape for the comparison endpoint. The models cover all six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` — comparison result model types (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod compare;` to expose the new module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each model struct derives `Serialize`, `Deserialize`, `Debug`, `Clone`.
- The `SbomComparisonResult` struct must include fields: `added_packages: Vec<AddedPackage>`, `removed_packages: Vec<RemovedPackage>`, `version_changes: Vec<VersionChange>`, `new_vulnerabilities: Vec<NewVulnerability>`, `resolved_vulnerabilities: Vec<ResolvedVulnerability>`, `license_changes: Vec<LicenseChange>`.
- Each sub-struct should match the API response shape from the Figma design context:
  - `AddedPackage`: name, version, license, advisory_count
  - `RemovedPackage`: same shape as AddedPackage
  - `VersionChange`: name, left_version, right_version, direction (enum: upgrade/downgrade)
  - `NewVulnerability`: advisory_id, severity, title, affected_package
  - `ResolvedVulnerability`: advisory_id, severity, title, previously_affected_package
  - `LicenseChange`: name, left_license, right_license
- Use `String` for text fields and `i32` or `u32` for counts, matching conventions in `modules/fundamental/src/sbom/model/summary.rs`.
- Per CONVENTIONS.md §Module pattern: place the new model file under the `model/` subdirectory of the `sbom` module, following the `model/ + service/ + endpoints/` structure. Applies: task creates `modules/fundamental/src/sbom/model/compare.rs` matching the convention's model module scope. See `modules/fundamental/src/sbom/model/summary.rs` for the established pattern.
- Reference existing types: `PackageSummary` in `modules/fundamental/src/package/model/summary.rs` for field naming conventions (e.g., `license` field), `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` for severity field naming.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct layout and serde derive patterns
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for severity field type and serialization
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reference for license field naming convention

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category fields
- [ ] All sub-structs (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) are defined with fields matching the API response shape
- [ ] All structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- [ ] The `compare` module is publicly exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] `cargo check` passes with no errors

## Test Requirements
- [ ] Verify serialization round-trip: create an `SbomComparisonResult` instance, serialize to JSON, deserialize back, and assert equality
- [ ] Verify the JSON output matches the expected API response shape (field names use snake_case)

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental model::compare` — model tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
