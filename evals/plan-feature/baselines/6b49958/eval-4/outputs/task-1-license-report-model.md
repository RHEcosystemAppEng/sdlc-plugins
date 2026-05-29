## Repository
trustify-backend

## Target Branch
main

## Description
Add the data model types for the license compliance report feature. This includes the `LicenseReport` response struct containing a vector of `LicenseGroup` entries, each with a license identifier, a list of packages under that license, and a boolean compliance flag. Also add a `LicensePolicy` struct for loading the configurable license policy from a JSON file, which defines allowed and denied license lists.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add re-exports for the new license report model types

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — define `LicenseReport`, `LicenseGroup`, and `PackageLicenseEntry` structs with serde Serialize/Deserialize derives
- `modules/fundamental/src/sbom/model/license_policy.rs` — define `LicensePolicy` struct with `allowed_licenses` and `denied_licenses` fields, plus a `load_from_file` constructor

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each model is a separate file with serde derives, re-exported from `mod.rs`.
- The `LicenseReport` struct should contain:
  - `groups: Vec<LicenseGroup>` — packages grouped by license
  - `total_packages: usize` — total packages analyzed
  - `compliant_count: usize` — number of compliant groups
  - `non_compliant_count: usize` — number of non-compliant groups
- The `LicenseGroup` struct should contain:
  - `license: String` — SPDX license identifier
  - `packages: Vec<PackageLicenseEntry>` — packages using this license
  - `compliant: bool` — whether this license complies with policy
- The `PackageLicenseEntry` struct should contain:
  - `name: String` — package name
  - `version: String` — package version
- The `LicensePolicy` struct should:
  - Load from a JSON file path using `serde_json::from_reader`
  - Contain `allowed_licenses: Option<Vec<String>>` and `denied_licenses: Option<Vec<String>>`
  - Implement a `is_compliant(&self, license: &str) -> bool` method: if `denied_licenses` is set and contains the license, return false; if `allowed_licenses` is set and does not contain the license, return false; otherwise return true
- Use the `PackageSummary` struct from `modules/fundamental/src/package/model/summary.rs` as reference for the package-level fields — it includes the `license` field that this feature depends on.
- Per constraints doc section 2 (Commit Rules): use Conventional Commits format, reference TC-9004 in the footer, include `--trailer="Assisted-by: Claude Code"`.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — demonstrates the serde derive pattern and struct layout used throughout the sbom module
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the `license` field that the compliance report depends on; reference for package-level data shape
- `common/src/model/paginated.rs::PaginatedResults` — demonstrates the response wrapper pattern, though the license report uses a custom response shape rather than pagination

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseGroup`, and `PackageLicenseEntry` structs are defined with serde Serialize/Deserialize derives
- [ ] `LicensePolicy` struct can load from a JSON configuration file
- [ ] `LicensePolicy::is_compliant` correctly evaluates allowed and denied license lists
- [ ] All new types are re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit test for `LicensePolicy::is_compliant` with a license on the denied list returning false
- [ ] Unit test for `LicensePolicy::is_compliant` with a license on the allowed list returning true
- [ ] Unit test for `LicensePolicy::is_compliant` with a license not on the allowed list returning false
- [ ] Unit test for `LicensePolicy::load_from_file` successfully loading a valid JSON policy file
- [ ] Unit test for `LicensePolicy::load_from_file` returning an error for a missing or invalid file

[sdlc-workflow] Description digest: sha256:29d270a6aa765d674356db216d7ea164e44f4fa1824f11562b72d07577d9073e
