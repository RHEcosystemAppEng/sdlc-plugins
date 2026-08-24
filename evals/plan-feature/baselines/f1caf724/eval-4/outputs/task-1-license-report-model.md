## Repository
trustify-backend

## Target Branch
main

## Description
Add model types for the license compliance report feature. Define `LicenseGroup`, `LicenseReport`, and `LicensePolicy` structs in the sbom model module. `LicenseReport` contains a vector of `LicenseGroup` entries, each grouping packages by license type and including a compliance flag. `LicensePolicy` defines allowlisted and denylisted licenses used for compliance checks. Also add a default license policy JSON configuration file.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod license_report;` declaration and re-export types

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- define `LicenseGroup`, `LicenseReport`, and `LicensePolicy` structs with serde Serialize/Deserialize derives
- `config/license-policy.json` -- default license policy configuration with common allowlisted licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) and denylisted licenses (GPL-3.0, AGPL-3.0)

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct definition conventions (derive macros, field visibility, documentation comments).
- `LicenseReport` response shape must match the Feature specification: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`. Map this to Rust: `LicenseReport { groups: Vec<LicenseGroup> }` and `LicenseGroup { license: String, packages: Vec<PackageLicenseEntry>, compliant: bool }`.
- `LicensePolicy` should support loading from a JSON config file at startup. Define fields: `allowed_licenses: Vec<String>`, `denied_licenses: Vec<String>`. A package is compliant if its license is not in the denied list (or is in the allowed list, depending on policy mode).
- The `PackageLicenseEntry` struct should include at minimum: package name, version, and purl to identify packages within each license group.
- Reference the existing `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` which already includes a license field -- this is the source data structure.
- Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ directory structure for the license report feature.
  Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's `.rs` module file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- reference for struct definition patterns (derive macros, field types)
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- contains the `license` field; source data type for license information
- `entity/src/package_license.rs` -- package-license mapping entity; defines the database relationship between packages and licenses

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseGroup`, `PackageLicenseEntry`, and `LicensePolicy` structs are defined with appropriate serde derives
- [ ] Types are exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Default license policy JSON file exists at `config/license-policy.json` with sensible defaults
- [ ] `LicensePolicy` can be deserialized from the JSON config file
- [ ] `LicenseReport` serialization matches the expected response shape from the Feature specification

## Test Requirements
- [ ] Unit test: `LicensePolicy` deserializes correctly from the default `config/license-policy.json`
- [ ] Unit test: `LicenseReport` serializes to the expected JSON shape `{ groups: [{ license, packages, compliant }] }`
- [ ] Unit test: `LicenseGroup` correctly represents a group of packages under a single license

## Verification Commands
- `cargo build -p trustify-fundamental` -- compiles without errors
- `cargo test -p trustify-fundamental -- license_report` -- model unit tests pass

## Dependencies
- None (first task in the chain)
