## Repository
trustify-backend

## Target Branch
main

## Description
Create response model structs for the license compliance report. The `LicenseReport` struct wraps a vector of `LicenseReportGroup` entries, where each group represents a distinct license type found in the SBOM. Each group lists the packages using that license and a boolean compliance flag based on the license policy.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReport` and `LicenseReportGroup` response structs with serde serialization

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to export the new module

## Implementation Notes
- Follow the existing response model pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) for struct shape and derives.
- `LicenseReportGroup` fields: `license: String`, `packages: Vec<PackageLicenseEntry>`, `compliant: bool`.
- `PackageLicenseEntry` fields: `name: String`, `version: String`, `purl: Option<String>`.
- The response shape matches the feature requirement: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`.
- Reference `modules/fundamental/src/package/model/summary.rs` (PackageSummary) for the package-level fields to include — the `license` field on PackageSummary shows the existing license data shape.
- Per CONVENTIONS.md §Response types: use the established struct pattern with serde derives. Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's Rust module scope.

## Acceptance Criteria
- [ ] `LicenseReport` struct contains a `groups: Vec<LicenseReportGroup>` field
- [ ] `LicenseReportGroup` contains `license`, `packages`, and `compliant` fields
- [ ] `PackageLicenseEntry` contains `name`, `version`, and optional `purl` fields
- [ ] All structs derive `Serialize` for JSON response rendering
- [ ] The serialized output matches the required response shape from the feature description

## Test Requirements
- [ ] Unit test: serialize a `LicenseReport` to JSON and verify the output structure
- [ ] Unit test: verify empty groups list serializes correctly

## Dependencies
- Depends on: Task 1 — License policy model
