## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Create the `SbomComparison` model struct and supporting diff category structs to represent the structured diff between two SBOMs. The model captures six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. This model is the response type for the comparison endpoint.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — SbomComparison struct with diff category fields

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod comparison;` to expose the new model module

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) for struct definition, derive macros, and serialization.

The `SbomComparison` struct should include:
- `added_packages: Vec<PackageDiff>` — packages in right SBOM but not left
- `removed_packages: Vec<PackageDiff>` — packages in left SBOM but not right
- `version_changes: Vec<VersionChange>` — packages with different versions
- `new_vulnerabilities: Vec<VulnerabilityDiff>` — advisories affecting right but not left
- `resolved_vulnerabilities: Vec<VulnerabilityDiff>` — advisories affecting left but not right
- `license_changes: Vec<LicenseChange>` — packages with changed licenses

Reference `PackageSummary` in `modules/fundamental/src/package/model/summary.rs` for the package field structure (includes license field). Reference `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` for advisory fields (includes severity).

Per CONVENTIONS.md §Module Pattern: follow model/ + service/ + endpoints/ structure for new domain additions.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's Rust module file scope.

Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for any fallible operations.
Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM model struct demonstrating derive macros and serialization patterns
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — package model with license field, reuse for diff category fields
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — advisory model with severity field, reuse for vulnerability diff

## Acceptance Criteria
- [ ] `SbomComparison` struct is defined with all six diff category fields
- [ ] Supporting structs (`PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`) are defined with appropriate fields
- [ ] All structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- [ ] Module is exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Structs can be serialized to JSON matching the expected response shape from the Figma design context
- [ ] Structs can be deserialized from JSON without error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
