## Repository
trustify-backend

## Target Branch
main

## Description
Define the response model structs for the license compliance report endpoint. The report groups packages by license type and includes a compliance flag per group, so the response shape needs `LicenseReport` (top-level wrapper) and `LicenseGroup` (per-license grouping with package list and compliance status).

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Define `LicenseReport` and `LicenseGroup` structs with serde Serialize/Deserialize derives

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to export the new module

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Response type definition (structs only; endpoint wired in a later task)

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct organization, derive macros, and documentation comments.

The `LicenseReport` struct should contain:
- `groups: Vec<LicenseGroup>` — list of license groupings
- `sbom_id: String` — reference to the source SBOM
- `total_packages: usize` — total package count
- `non_compliant_count: usize` — count of non-compliant groups

The `LicenseGroup` struct should contain:
- `license: String` — SPDX license identifier
- `packages: Vec<PackageSummary>` — packages with this license (reuse `PackageSummary` from `modules/fundamental/src/package/model/summary.rs`)
- `compliant: bool` — whether this license passes the configured policy

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct patterns, derive macros, and serde annotations
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reuse directly as the package type within each license group

## Acceptance Criteria
- [ ] `LicenseReport` struct is defined with `groups`, `sbom_id`, `total_packages`, and `non_compliant_count` fields
- [ ] `LicenseGroup` struct is defined with `license`, `packages`, and `compliant` fields
- [ ] Both structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- [ ] `PackageSummary` is reused from the existing package model (not redefined)
- [ ] Module is exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Structs can be serialized to JSON matching the expected response shape: `{ "sbom_id": "...", "groups": [{ "license": "MIT", "packages": [...], "compliant": true }], "total_packages": 5, "non_compliant_count": 0 }`
- [ ] Structs can be deserialized from valid JSON without error

[sdlc-workflow] Description digest: sha256-md:07106c2d7bb8e2d3fbeeded73475a49ea1b6378ce332a7ba73e1f9e1984053f6
