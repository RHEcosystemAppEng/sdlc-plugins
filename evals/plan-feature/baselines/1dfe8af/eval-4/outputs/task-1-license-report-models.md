## Repository
trustify-backend

## Target Branch
main

## Description
Add the response model structs for the license compliance report. This includes a `LicenseReport` top-level struct containing a vector of `LicenseGroup` entries, where each group represents a single license identifier (e.g., "MIT", "Apache-2.0") along with its list of packages and a `compliant` boolean flag. These structs will be used by the service layer and endpoint handler in subsequent tasks.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Define `LicenseReport` and `LicenseGroup` structs with serde Serialize/Deserialize derives

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` and re-export the new types

## Implementation Notes
- Follow the existing model pattern seen in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs`.
- `LicenseGroup` should contain: `license: String`, `packages: Vec<PackageRef>`, `compliant: bool`.
- `PackageRef` is a lightweight reference struct with `name: String`, `version: String`, `purl: Option<String>` — just enough to identify a package in the report without duplicating the full `PackageSummary`.
- `LicenseReport` should contain: `sbom_id: String`, `groups: Vec<LicenseGroup>`, `total_packages: usize`, `non_compliant_count: usize`.
- All structs derive `serde::Serialize`, `serde::Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema` for OpenAPI generation.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference for struct conventions, derives, and serde attributes used in the SBOM module
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Contains the `license` field; reference for how license data is represented in existing models

## Acceptance Criteria
- [ ] `LicenseReport` and `LicenseGroup` structs compile and are publicly exported from the sbom model module
- [ ] Structs derive Serialize, Deserialize, Clone, Debug, and ToSchema
- [ ] `LicenseGroup` includes `license`, `packages`, and `compliant` fields
- [ ] `LicenseReport` includes `sbom_id`, `groups`, `total_packages`, and `non_compliant_count` fields

## Test Requirements
- [ ] Unit test confirming `LicenseReport` serializes to expected JSON structure
- [ ] Unit test confirming `LicenseGroup` with `compliant: false` serializes correctly

[sdlc-workflow] Description digest: sha256-md:ccdc5f430f099f81e604de018ea6f6e07801b202a36389c7fa8710cf21f6c73f
