# Task 2 -- Add license compliance report model structs

**Summary:** Add license compliance report response model structs

**Priority:** Major
**Fix Versions:** RHTPA 1.5.0
**Labels:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
main

## Description
Define the response model structs for the license compliance report. These structs represent the grouped license data returned by the `GET /api/v2/sbom/{id}/license-report` endpoint, including per-license-group compliance flags.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- `LicenseReportGroup` and `LicenseReport` structs with serde serialization

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod license_report` to expose the new model

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/` -- see `summary.rs` (`SbomSummary`) and `details.rs` (`SbomDetails`) for the struct layout, derive macros, and serialization approach
- Define the following structs:
  - `LicenseReportGroup`: fields `license: String` (SPDX identifier), `packages: Vec<PackageLicenseEntry>`, `compliant: bool`
  - `PackageLicenseEntry`: fields `name: String`, `version: String`, `purl: Option<String>` (package URL for identification)
  - `LicenseReport`: fields `sbom_id: String`, `groups: Vec<LicenseReportGroup>`, `total_packages: usize`, `compliant_count: usize`, `non_compliant_count: usize`
- All structs should derive `serde::Serialize`, `Clone`, `Debug`, and `utoipa::ToSchema` (for OpenAPI generation) consistent with sibling model structs
- The response shape must match the feature requirement: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- Per CONVENTIONS.md (Key Conventions -- Error handling): use `Result<T, AppError>` with `.context()` wrapping for any fallible operations. Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- reference for struct layout and derive macros
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` -- reference for struct layout
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- contains the `license` field, relevant for understanding the package-license data model

## Acceptance Criteria
- [ ] `LicenseReport` and `LicenseReportGroup` structs serialize to the expected JSON shape
- [ ] All structs derive necessary traits (Serialize, Clone, Debug, ToSchema)
- [ ] Module is properly exported from `sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test: `LicenseReport` serializes to expected JSON structure with groups, compliance flags, and counts
- [ ] Unit test: empty report (no groups) serializes correctly

## Dependencies
- None
