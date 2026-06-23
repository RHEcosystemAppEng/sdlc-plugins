# Task 1 — Add license compliance report model types

## Repository
trustify-backend

## Target Branch
main

## Description
Define the model types for the license compliance report feature. These types represent the structured response for the `GET /api/v2/sbom/{id}/license-report` endpoint: a report containing license groups, each listing packages under that license and a compliance flag indicating whether the license complies with the configured policy.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export new license report model types

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — define `LicenseReport`, `LicenseGroup`, and `LicensePackageRef` structs

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each model is a standalone file in the `model/` directory, re-exported from `mod.rs`.
- Define the following structs with `Serialize` and `Deserialize` derives:
  - `LicenseReport` — top-level response containing `groups: Vec<LicenseGroup>`
  - `LicenseGroup` — represents one license type: `license: String`, `packages: Vec<LicensePackageRef>`, `compliant: bool`
  - `LicensePackageRef` — reference to a package: `name: String`, `version: String`, `purl: Option<String>`
- Use `utoipa::ToSchema` derive for OpenAPI schema generation if the existing models use it.
- The `compliant` field on `LicenseGroup` will be populated by the service layer (Task 2); at the model level it is simply a boolean field.
- Reference the existing `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` which includes a `license` field — this confirms the data model supports license information on packages.
- Per docs/constraints.md section 5 (Code Change Rules): changes must be scoped to listed files; inspect code before modifying; follow patterns in Implementation Notes.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — follow the same struct layout, derive macros, and serialization approach
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the `license` field that downstream service logic will read from
- `common/src/model/paginated.rs::PaginatedResults` — reference for response wrapper patterns, though the license report uses a non-paginated response

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseGroup`, and `LicensePackageRef` structs are defined with appropriate fields
- [ ] Structs derive `Serialize`, `Deserialize`, and any other macros consistent with existing models
- [ ] Types are re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors (`cargo check`)

## Test Requirements
- [ ] Unit test verifying `LicenseReport` serializes to the expected JSON structure: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`
- [ ] Unit test verifying deserialization round-trip for `LicenseReport`

## Dependencies
- None

sha256-md:4297e7a4768664538f71438140415bff62f27da1b0a47b7e078dd85fdfd4d6e4
