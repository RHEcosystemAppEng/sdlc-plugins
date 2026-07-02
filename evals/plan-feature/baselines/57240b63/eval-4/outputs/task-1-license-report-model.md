## Repository
trustify-backend

## Target Branch
main

## Description
Define the response model types for the license compliance report endpoint. This includes the top-level `LicenseReport` struct containing a vector of `LicenseGroup` entries, where each group represents a license type with its associated packages and a compliance flag. These types form the contract for the `GET /api/v2/sbom/{id}/license-report` response.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- LicenseReport, LicenseGroup, and PackageLicenseEntry response structs with Serialize derives

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod license_report;` to expose the new module

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) for struct layout and derive macros.
- `LicenseReport` fields: `groups: Vec<LicenseGroup>`, `compliant: bool` (overall compliance summary -- false if any group is non-compliant).
- `LicenseGroup` fields: `license: String` (SPDX identifier), `packages: Vec<PackageLicenseEntry>`, `compliant: bool`.
- `PackageLicenseEntry` fields: `name: String`, `version: String`, `purl: Option<String>`.
- All structs must derive `serde::Serialize` and `utoipa::ToSchema` for OpenAPI documentation, consistent with existing model types in the sbom/model/ directory.
- Reference `entity/src/package.rs` and `entity/src/package_license.rs` for the underlying database entity field names to ensure model fields align with entity columns.

- Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ directory structure for the license report feature.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's model directory scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- reference for struct layout, derive macros, and serde attributes
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` -- reference for nested struct composition patterns
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- contains the `license` field; reference for package-level data representation

## Acceptance Criteria
- [ ] `LicenseReport` struct is defined with `groups: Vec<LicenseGroup>` and `compliant: bool`
- [ ] `LicenseGroup` struct is defined with `license: String`, `packages: Vec<PackageLicenseEntry>`, `compliant: bool`
- [ ] `PackageLicenseEntry` struct is defined with `name: String`, `version: String`, `purl: Option<String>`
- [ ] All structs derive `Serialize` and `ToSchema`
- [ ] Module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Project compiles without errors (`cargo check`)

## Test Requirements
- [ ] `cargo check` passes with the new model types
- [ ] Structs can be serialized to JSON matching the expected response shape: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }], "compliant": true }`

## Verification Commands
- `cargo check -p trustify-module-fundamental` -- expected: compiles without errors

## Dependencies
- None

---

[sdlc-workflow] Description digest: sha256-md:bd952abab2ffeff8756f1dce030d9a6fae4def93c477e87b52c0e95b35387a4a
