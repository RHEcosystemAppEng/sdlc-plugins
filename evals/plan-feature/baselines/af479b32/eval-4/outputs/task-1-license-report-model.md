# Task 1 — Add license report response model types

**Summary:** Add license report response model types

**Epic:** TC-9004: License report data layer

## Repository
trustify-backend

## Target Branch
main

## Description
Add the response model types for the license compliance report endpoint. These structs define the shape of the `GET /api/v2/sbom/{id}/license-report` response: a top-level `LicenseReport` containing a vector of `LicenseReportGroup` entries, each grouping packages by license type with a compliance flag.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — defines `LicenseReportGroup` and `LicenseReport` structs with Serialize derive

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod license_report` and re-export the new types

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `LicenseReport { groups: Vec<LicenseReportGroup> }` where each group contains `{ license: String, packages: Vec<PackageLicenseEntry>, compliant: bool }`

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs`. Each model struct derives `Serialize` (and optionally `Deserialize`) and lives in its own file under the `model/` directory.
- The `LicenseReport` struct should contain:
  - `groups: Vec<LicenseReportGroup>` — packages grouped by license
- The `LicenseReportGroup` struct should contain:
  - `license: String` — the SPDX license identifier
  - `packages: Vec<PackageLicenseEntry>` — packages using this license
  - `compliant: bool` — whether this license is compliant with the configured policy
- Define a `PackageLicenseEntry` struct with at minimum:
  - `name: String` — package name
  - `version: String` — package version
  - `transitive: bool` — whether this is a transitive dependency
- Reference the existing `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` which already includes a `license` field — reuse its field naming conventions.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — demonstrates the established model struct pattern (derives, field types, module registration)
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the existing `license` field definition; reference for field naming and type conventions
- `common/src/model/paginated.rs::PaginatedResults` — demonstrates the response wrapper pattern used by other endpoints

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseReportGroup`, and `PackageLicenseEntry` structs are defined with appropriate derives
- [ ] Structs are publicly exported from the sbom model module
- [ ] The response shape matches the specification: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Verify that the model types can be serialized to JSON matching the expected response shape
- [ ] Verify that an empty groups vector serializes correctly
- [ ] Verify that the `compliant` field is correctly included in serialization

## Dependencies
- None
