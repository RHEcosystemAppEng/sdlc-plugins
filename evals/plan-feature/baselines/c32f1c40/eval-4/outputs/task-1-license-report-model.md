## Repository
trustify-backend

## Target Branch
main

## Description
Add license compliance report response types to the SBOM model layer. These structs represent the grouped license report response returned by the new `GET /api/v2/sbom/{id}/license-report` endpoint. The response groups packages by license type and includes a compliance flag per group.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Define `LicenseReportGroup` and `LicenseReport` response structs with serde serialization

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` and re-export the new types

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct conventions and serde derives.
- `LicenseReport` should contain a `groups` field of type `Vec<LicenseReportGroup>`.
- `LicenseReportGroup` should contain:
  - `license: String` — the SPDX license identifier
  - `packages: Vec<PackageSummary>` — list of packages with this license (reuse `PackageSummary` from `modules/fundamental/src/package/model/summary.rs`)
  - `compliant: bool` — whether this license group complies with the configured policy
- Derive `Serialize`, `Deserialize`, `Debug`, and `Clone` on both structs.
- Per Key Conventions (Module pattern): each domain module follows `model/ + service/ + endpoints/` structure. This task adds to the model layer.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's Rust module file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct layout and serde derives
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — reference for nested response types
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reuse as the package type within `LicenseReportGroup.packages`

## Acceptance Criteria
- [ ] `LicenseReportGroup` struct exists with `license`, `packages`, and `compliant` fields
- [ ] `LicenseReport` struct exists with a `groups` field of type `Vec<LicenseReportGroup>`
- [ ] Both structs derive `Serialize`, `Deserialize`, `Debug`, and `Clone`
- [ ] `modules/fundamental/src/sbom/model/mod.rs` re-exports the new types
- [ ] The response shape matches the specification: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Test Requirements
- [ ] Unit test verifying `LicenseReport` serializes to the expected JSON shape
- [ ] Unit test verifying `LicenseReportGroup` with `compliant: true` and `compliant: false` values serialize correctly
- [ ] Verify `PackageSummary` from the package module is compatible as a field type

## Dependencies
- None (this is the first task in the chain)
