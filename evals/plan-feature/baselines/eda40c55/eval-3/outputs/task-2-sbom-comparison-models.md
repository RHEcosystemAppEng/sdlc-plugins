## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the Rust model types for the SBOM comparison diff response. These structs represent the structured diff between two SBOMs and will be serialized as the response body for the new `GET /api/v2/sbom/compare` endpoint. The models cover six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

No new database tables are required -- the comparison is computed on-the-fly from existing package, advisory, and license data.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` -- SBOM comparison diff model types

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod comparison;` to export the new module

## Implementation Notes
- Define the following structs, all deriving `Serialize`, `Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema`:
  - `SbomComparison` -- top-level response containing all six diff category vectors
  - `AddedPackage` -- fields: `name: String`, `version: String`, `license: String`, `advisory_count: u32`
  - `RemovedPackage` -- fields: `name: String`, `version: String`, `license: String`, `advisory_count: u32`
  - `VersionChange` -- fields: `name: String`, `left_version: String`, `right_version: String`, `direction: VersionChangeDirection`
  - `VersionChangeDirection` -- enum with variants `Upgrade`, `Downgrade`
  - `NewVulnerability` -- fields: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`
  - `ResolvedVulnerability` -- fields: `advisory_id: String`, `severity: String`, `title: String`, `previously_affected_package: String`
  - `LicenseChange` -- fields: `name: String`, `left_license: String`, `right_license: String`
- Follow the existing model structure in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs` for derive macros, imports, and documentation patterns.
- Per CONVENTIONS.md §Module Pattern: follow the `model/ + service/ + endpoints/` module structure for the comparison feature. Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's model file scope.
- Reference the existing `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` for field naming conventions (e.g., `license` field) and the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` for severity field conventions.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- existing SBOM model struct demonstrating the derive macro pattern and Serde configuration
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- package model with `license` field showing the naming convention
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- advisory model with `severity` field showing the naming convention

## Acceptance Criteria
- [ ] `SbomComparison` struct and all six diff-category structs compile successfully
- [ ] All structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema`
- [ ] The `comparison` module is exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Field names match the API response shape specified in the feature description (`added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`)

## Test Requirements
- [ ] Verify the comparison model types serialize to the expected JSON shape using `serde_json::to_value`
- [ ] Verify `VersionChangeDirection` serializes as lowercase strings (`"upgrade"`, `"downgrade"`)

## Verification Commands
- `cargo check -p trustify-module-fundamental` -- compiles without errors
- `cargo test -p trustify-module-fundamental model::comparison` -- model serialization tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
