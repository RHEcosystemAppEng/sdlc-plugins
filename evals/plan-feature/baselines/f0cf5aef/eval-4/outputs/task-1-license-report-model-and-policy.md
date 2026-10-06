## Repository
trustify-backend

## Target Branch
main

## Description
Add the model types and policy configuration structures for the license compliance report feature. This task creates the data types that represent a grouped license report (licenses with their associated packages and compliance status) and the configurable license policy (allowed/denied license lists). The policy is loaded from a JSON configuration file in the repository.

This is the foundational layer for TC-9004 — subsequent tasks build the service logic and API endpoint on top of these types.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — export the new `license_report` module

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseGroup, LicenseReport, and CompliancePolicy structs with serde Serialize/Deserialize derives
- `license-policy.json` — default license policy configuration file (allowed and denied license SPDX identifiers)

## API Changes
- None (model-only task; the endpoint is added in Task 3)

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) — structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`.
- The `LicenseReport` struct should contain a `groups` field: `Vec<LicenseGroup>` where each `LicenseGroup` has `license: String`, `packages: Vec<PackageLicenseEntry>`, and `compliant: bool`.
- The `CompliancePolicy` struct should define `allowed_licenses: Option<Vec<String>>` and `denied_licenses: Option<Vec<String>>` with SPDX identifiers. When `denied_licenses` contains a license, that group's `compliant` flag is `false`. When `allowed_licenses` is set, only licenses in that list are compliant.
- The `PackageLicenseEntry` struct should contain the package name, version, and purl — reuse the fields from `PackageSummary` in `modules/fundamental/src/package/model/summary.rs`.
- Per CONVENTIONS.md Key Conventions: use SeaORM for database types. Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's Rust module scope.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the `license` field; reuse field structure for PackageLicenseEntry
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct derive patterns and serde annotations
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — reference for model struct organization

## Acceptance Criteria
- [ ] `LicenseReport` struct exists with `groups: Vec<LicenseGroup>` field
- [ ] `LicenseGroup` struct exists with `license: String`, `packages: Vec<PackageLicenseEntry>`, `compliant: bool` fields
- [ ] `CompliancePolicy` struct exists with `allowed_licenses` and `denied_licenses` fields, deserializable from JSON
- [ ] `PackageLicenseEntry` struct exists with package name, version, and purl fields
- [ ] Default `license-policy.json` configuration file exists in the repository root
- [ ] All structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`
- [ ] `license_report` module is exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] `CompliancePolicy` can be deserialized from the default `license-policy.json` file
- [ ] `LicenseReport` can be serialized to JSON matching the expected response shape `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- [ ] `CompliancePolicy` with only `denied_licenses` correctly identifies denied licenses
- [ ] `CompliancePolicy` with only `allowed_licenses` correctly identifies non-allowed licenses

## Dependencies
- None (this is the first task in the implementation sequence)
