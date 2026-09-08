## Repository
trustify-backend

## Target Branch
main

## Description
Define the response model types for the license compliance report endpoint and the license policy configuration schema. The license report groups packages by license type and flags non-compliant licenses based on a configurable policy stored as a JSON configuration file in the repository.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add module declaration for license_report
- `common/src/model/mod.rs` -- add module declaration for license_policy

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- LicenseReportGroup and LicenseReport response structs with serde Serialize/Deserialize derives
- `common/src/model/license_policy.rs` -- LicensePolicy struct for parsing the JSON policy config file, with a method to check license compliance

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct conventions (derive macros, field naming)
- The `LicenseReport` struct should contain a `groups` field: `Vec<LicenseReportGroup>`
- Each `LicenseReportGroup` should have: `license: String`, `packages: Vec<PackageSummary>`, `compliant: bool`
- The `LicensePolicy` struct should define a list of allowed/denied license identifiers and a method `is_compliant(license: &str) -> bool`
- Reference the SPDX license identifier format for license string matching
- Per CONVENTIONS.md Module pattern: follow the `model/ + service/ + endpoints/` structure for new module files.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's module file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- example of model struct conventions (derives, field types)
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- the package model type that includes the license field; reuse this in the report groups
- `entity/src/package_license.rs` -- the existing Package-License mapping entity that underlies license data

## Acceptance Criteria
- [ ] `LicenseReportGroup` struct defined with `license`, `packages`, and `compliant` fields
- [ ] `LicenseReport` struct defined with `groups: Vec<LicenseReportGroup>`
- [ ] `LicensePolicy` struct defined with configurable allowed/denied license lists
- [ ] `LicensePolicy::is_compliant()` method correctly checks a license against the policy
- [ ] All structs derive `Serialize` and `Deserialize`
- [ ] Module declarations added to parent `mod.rs` files

## Test Requirements
- [ ] Unit test for `LicensePolicy::is_compliant()` with allowed license returns true
- [ ] Unit test for `LicensePolicy::is_compliant()` with denied license returns false
- [ ] Unit test for `LicensePolicy` deserialization from JSON config string

## Dependencies
- None
