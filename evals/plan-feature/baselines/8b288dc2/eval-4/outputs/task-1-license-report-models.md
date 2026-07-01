## Repository
trustify-backend

## Target Branch
main

## Description
Add model types for the license compliance report feature. This includes the response structs for the license report endpoint: `LicenseReportGroup` (representing a group of packages sharing the same license with a compliance flag) and `LicenseReport` (the top-level response containing a list of groups). Also add a `LicensePolicy` struct for loading the configurable license policy from a JSON file.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add module declarations for new report model files

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- define `LicenseReport` and `LicenseReportGroup` response structs with serde Serialize/Deserialize
- `modules/fundamental/src/sbom/model/license_policy.rs` -- define `LicensePolicy` struct with a list of allowed/denied license SPDX identifiers, loaded from JSON config

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` -- each model is a standalone file with structs deriving `Serialize`, `Deserialize`, `Clone`, `Debug`.
- `LicenseReportGroup` should contain: `license: String` (the SPDX license identifier), `packages: Vec<PackageLicenseEntry>` (list of packages with this license), `compliant: bool` (whether this license is compliant with the policy).
- `LicenseReport` should contain: `groups: Vec<LicenseReportGroup>`.
- `PackageLicenseEntry` should contain package identifier fields (name, version) drawn from the existing `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs`.
- `LicensePolicy` should support both allowlist and denylist modes for license compliance checking.
- Reference the existing `package_license` entity in `entity/src/package_license.rs` for understanding how license data is currently stored.
- Per CONVENTIONS.md (Key Conventions): all response types follow the module `model/` pattern with serde derives.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's `.rs` model file scope.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- contains license field and package identification fields that can inform `PackageLicenseEntry` structure
- `entity/src/package_license.rs` -- Package-License mapping entity that defines the underlying data model
- `common/src/model/paginated.rs::PaginatedResults` -- response wrapper pattern to follow for struct design conventions

## Acceptance Criteria
- [ ] `LicenseReport` and `LicenseReportGroup` structs are defined with proper serde derives
- [ ] `LicensePolicy` struct can be deserialized from a JSON configuration file
- [ ] `PackageLicenseEntry` struct captures package name, version, and license identifier
- [ ] All new types are re-exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test for `LicensePolicy` deserialization from valid JSON
- [ ] Unit test for `LicensePolicy` deserialization error on invalid JSON
- [ ] Unit test for `LicenseReport` serialization produces expected JSON structure

## Dependencies
- None

## Description Digest
sha256-md:cc0ce990c78f95c2469b66d18dd866684f646f421e50a26652004ca55f6894df
