## Repository
trustify-backend

## Target Branch
main

## Description
Define the response model structs for the license compliance report endpoint. This includes a `LicenseReport` struct containing a vector of `LicenseGroup` entries, where each group represents a single license type with its associated packages and a compliance flag. These structs will be serialized as JSON responses from the endpoint.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Define `LicenseReport` and `LicenseGroup` structs with serde Serialize/Deserialize derives, following the pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new model module

## Implementation Notes
- Follow the struct pattern from `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) for derive macros and field organization
- The `LicenseGroup` struct should contain: `license: String`, `packages: Vec<PackageRef>`, `compliant: bool`
- The `LicenseReport` struct should contain: `groups: Vec<LicenseGroup>`, `total_packages: usize`, `non_compliant_count: usize`
- Define a `PackageRef` struct with `name: String`, `version: String` to reference packages within each group
- Use `#[derive(Debug, Clone, Serialize, Deserialize)]` consistent with existing model structs
- The `PackageSummary` struct in `modules/fundamental/src/sbom/model/../../../package/model/summary.rs` includes a `license` field that confirms license data is already modeled in the system

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseGroup`, and `PackageRef` structs are defined with appropriate serde derives
- [ ] Module is exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Structs compile without errors

## Test Requirements
- [ ] Unit tests verify that `LicenseReport` serializes to the expected JSON shape: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }], "total_packages": N, "non_compliant_count": N }`
- [ ] Unit tests verify deserialization round-trip

## Digest
[sdlc-workflow] Description digest: sha256-md:be4a7428b81b6335fd3a5e8e898ea0fab1a9977dd7af90679372c3b47c2ca541
