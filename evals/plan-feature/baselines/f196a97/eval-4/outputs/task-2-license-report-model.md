# Task 2 — Add license report response model

## Repository
trustify-backend

## Target Branch
main

## Description
Add the response model structs for the license compliance report endpoint. The report groups packages by license type and flags non-compliant groups based on the license policy. This model is consumed by both the service layer and the endpoint handler.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReport and LicenseGroup structs for the compliance report response

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to export the new module

## Implementation Notes
- Follow the existing model patterns in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — use `#[derive(Debug, Clone, Serialize, Deserialize)]` with serde
- The response structure must match the specification: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- Define these structs:
  - `LicenseReport` — top-level response containing `groups: Vec<LicenseGroup>`
  - `LicenseGroup` — contains `license: String` (SPDX identifier), `packages: Vec<PackageLicenseEntry>`, `compliant: bool`
  - `PackageLicenseEntry` — contains package identifiers (name, version, purl) sufficient to identify a package in the SBOM context
- Reference the `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` which already includes a `license` field — reuse or align field naming with this existing model
- Use the `entity/src/package.rs` and `entity/src/package_license.rs` entity definitions to understand the underlying data model

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Already has a `license` field; align field naming for consistency
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Follow its struct and derive patterns

## Acceptance Criteria
- [ ] LicenseReport struct serializes to the specified JSON shape: `{ groups: [{ license, packages, compliant }] }`
- [ ] LicenseGroup correctly represents a single license grouping with compliance status
- [ ] PackageLicenseEntry contains sufficient package identification fields

## Test Requirements
- [ ] Unit test: serialize a LicenseReport with multiple groups and verify JSON output matches the expected shape
- [ ] Unit test: verify empty report (no groups) serializes correctly

## Dependencies
- None
