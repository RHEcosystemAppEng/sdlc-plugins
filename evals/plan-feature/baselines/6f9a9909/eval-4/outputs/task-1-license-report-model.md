## Repository
trustify-backend

## Target Branch
main

## Description
Add the response model types for the license compliance report endpoint. This task creates the data structures that represent a license compliance report: the top-level report response containing groups of packages organized by license type, with compliance flags indicating whether each license group conforms to the project's declared policy.

These model types are consumed by the license report service (Task 3) and serialized as JSON by the license report endpoint (Task 4).

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- defines LicenseReportResponse, LicenseGroup, and LicensePackageEntry structs with serde Serialize/Deserialize derives

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod license_report;` to expose the new model module

## Implementation Notes
- Follow the existing model struct patterns in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) for derive macros, field naming, and documentation style.
- The response shape per the feature requirements is: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`. Define structs that serialize to this shape.
- `LicenseReportResponse` should contain a `groups` field of type `Vec<LicenseGroup>`.
- `LicenseGroup` should contain: `license: String`, `packages: Vec<LicensePackageEntry>`, `compliant: bool`.
- `LicensePackageEntry` should contain at minimum the package identifier fields (name, version) from the existing `PackageSummary` in `modules/fundamental/src/package/model/summary.rs`.
- Use `#[derive(Clone, Debug, Serialize, Deserialize, utoipa::ToSchema)]` to maintain consistency with existing model types and enable OpenAPI schema generation.
- Per CONVENTIONS.md Module pattern: follow the `model/ + service/ + endpoints/` structure for the sbom domain module.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's module directory structure scope.

### Constraints (from docs/constraints.md)
- SS5.1: Keep changes scoped to the files listed in Files to Modify and Files to Create.
- SS5.2: Inspect existing model files before writing new ones to follow established patterns.
- SS2.1: Commit must reference Jira issue ID in footer.
- SS2.2: Use Conventional Commits format.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- reference for struct derive macros and field naming conventions
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- contains the `license` field; reuse field definitions for LicensePackageEntry

## Acceptance Criteria
- [ ] `LicenseReportResponse`, `LicenseGroup`, and `LicensePackageEntry` structs are defined in `modules/fundamental/src/sbom/model/license_report.rs`
- [ ] Structs derive Serialize, Deserialize, and ToSchema for OpenAPI compatibility
- [ ] The model module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Response shape matches the specification: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- [ ] Code compiles without warnings

## Test Requirements
- [ ] Unit test verifying LicenseReportResponse serializes to the expected JSON structure
- [ ] Unit test verifying deserialization round-trip for LicenseReportResponse

## Dependencies
- None (this is the foundational model task)
