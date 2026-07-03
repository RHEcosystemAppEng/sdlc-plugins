## Repository

trustify-backend

## Target Branch

main

## Description

Define the response models for the license compliance report endpoint. This task introduces the data structures that represent a grouped license report, individual license groups, and the license policy configuration. These models follow the existing module pattern used by `SbomSummary`, `SbomDetails`, and `PackageSummary`.

## Files to Modify

- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new license report model module

## Files to Create

- `modules/fundamental/src/sbom/model/license_report.rs` — defines `LicenseReport`, `LicenseReportGroup`, and `PackageLicenseEntry` structs with serde Serialize/Deserialize derives
- `common/src/model/license_policy.rs` — defines `LicensePolicy` and `LicensePolicyRule` structs for the configurable compliance policy

## Implementation Notes

- Follow the struct patterns in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for response model conventions (derive macros, field naming)
- `LicenseReport` should contain a `groups: Vec<LicenseReportGroup>` field as specified in the requirements
- Each `LicenseReportGroup` should contain: `license: String`, `packages: Vec<PackageLicenseEntry>`, `compliant: bool`
- `PackageLicenseEntry` should reference the package name and version, mirroring fields from `entity/src/package.rs` and `modules/fundamental/src/package/model/summary.rs`
- `LicensePolicy` should be deserializable from JSON and contain a list of `LicensePolicyRule` entries, each specifying a license identifier and whether it is allowed or denied
- Register the new `license_policy` module in `common/src/model/mod.rs`
- All structs must derive `Clone`, `Debug`, `Serialize`, `Deserialize` and use `#[serde(rename_all = "camelCase")]` consistent with existing models

## Acceptance Criteria

- `LicenseReport`, `LicenseReportGroup`, and `PackageLicenseEntry` structs compile and are publicly exported from the sbom model module
- `LicensePolicy` and `LicensePolicyRule` structs compile and are publicly exported from the common model module
- All structs derive the standard trait set (Clone, Debug, Serialize, Deserialize)
- `cargo check` passes with no errors

## Test Requirements

- Unit tests in `license_report.rs` verifying serialization round-trip for `LicenseReport` (serialize to JSON and deserialize back)
- Unit test verifying `LicensePolicy` deserialization from a sample JSON string
