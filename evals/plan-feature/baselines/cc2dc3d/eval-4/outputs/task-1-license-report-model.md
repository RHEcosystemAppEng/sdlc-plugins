## Repository
trustify-backend

## Target Branch
main

## Description
Add model structs for the license compliance report feature. This task creates the data structures that represent a license compliance report: `LicenseReport` (the top-level response), `LicenseGroup` (packages grouped by license type with a compliance flag), and `LicensePolicy` (the configurable policy defining allowed and denied licenses). These models will be consumed by the service layer (Task 2) and the endpoint (Task 3).

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReport, LicenseGroup, and LicensePolicy structs with serde Serialize/Deserialize derives

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod license_report;` to expose the new module

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each model file defines a struct with serde derives and field documentation.
- The `LicenseReport` struct should contain a `groups` field of type `Vec<LicenseGroup>`.
- The `LicenseGroup` struct should contain: `license: String` (the SPDX license identifier), `packages: Vec<PackageRef>` (references to packages with this license), and `compliant: bool` (whether this license is allowed by the policy).
- The `LicensePolicy` struct should support a list of denied license identifiers and optionally a list of explicitly allowed identifiers, deserializable from a JSON configuration file.
- Reference the `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` which includes a `license` field — this is the existing data source for package license information.
- Use `serde::Serialize` and `serde::Deserialize` derives consistent with existing model patterns.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — demonstrates the established model struct pattern with serde derives
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — demonstrates a more complex model struct with nested types
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the `license` field that the report will aggregate; the report model should reference or embed package information compatible with this type

## Acceptance Criteria
- [ ] `LicenseReport` struct exists with a `groups: Vec<LicenseGroup>` field
- [ ] `LicenseGroup` struct exists with `license`, `packages`, and `compliant` fields
- [ ] `LicensePolicy` struct exists and can be deserialized from JSON
- [ ] All structs derive `Serialize` and `Deserialize`
- [ ] The module is publicly exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit test verifying `LicenseReport` can be serialized to JSON in the expected format: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`
- [ ] Unit test verifying `LicensePolicy` can be deserialized from a JSON configuration string
- [ ] Unit test verifying `LicenseGroup` correctly represents a group with compliance flag

## Verification Commands
- `cargo build -p trustify-fundamental` — should compile without errors
- `cargo test -p trustify-fundamental license_report` — should pass all unit tests
