# Task 2 -- Add license compliance report model

## Repository
trustify-backend

## Target Branch
main

## Description
Add the response model for the license compliance report endpoint. The model represents packages grouped by license type with compliance flags, matching the API contract specified in the feature: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- LicenseReportGroup and LicenseReport structs for the grouped license compliance response

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod license_report;` to expose the new module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/` -- see `summary.rs` (SbomSummary) and `details.rs` (SbomDetails) for the established struct pattern in this module.
- Define the following structs:
  - `LicenseReportGroup` -- represents a single license group containing:
    - `license: String` -- the SPDX license identifier
    - `packages: Vec<PackageRef>` -- list of packages with this license (include package name, version, and purl)
    - `compliant: bool` -- whether this license group is compliant with the policy
  - `LicenseReport` -- the top-level response containing:
    - `groups: Vec<LicenseReportGroup>` -- all license groups
    - `sbom_id: String` -- the SBOM this report was generated for
    - `policy_name: String` -- which policy was applied (for traceability)
- All structs must derive `Serialize` and `Deserialize` using serde, plus `Clone`, `Debug`, `PartialEq` per project conventions for model structs.
- The `PackageRef` inner struct should reference `PackageSummary` fields from `modules/fundamental/src/package/model/summary.rs` -- use a lightweight projection rather than embedding the full `PackageSummary` to keep the response lean.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs` -- SbomSummary struct; follow same derive macro and field documentation pattern
- `modules/fundamental/src/sbom/model/details.rs` -- SbomDetails struct; demonstrates the detail-level model pattern
- `modules/fundamental/src/package/model/summary.rs` -- PackageSummary struct (includes `license` field); reference for the package data shape

## Acceptance Criteria
- [ ] `LicenseReport` struct serializes to the response shape specified in the feature: `{ groups: [{ license: "...", packages: [...], compliant: true/false }] }`
- [ ] `LicenseReportGroup` includes license name, package list, and compliance flag
- [ ] Model structs derive appropriate traits (Serialize, Deserialize, Clone, Debug, PartialEq)

## Test Requirements
- [ ] Unit test: `LicenseReport` serializes to expected JSON structure
- [ ] Unit test: `LicenseReportGroup` with compliant=true and compliant=false both serialize correctly
- [ ] Unit test: round-trip serialization/deserialization of `LicenseReport`

## Verification Commands
- `cargo test -p fundamental` -- all tests pass including new license report model tests

## Dependencies
- Depends on: Task 1 -- Add license policy configuration model and loader (uses `LicensePolicy` for the `policy_name` field and compliance evaluation context)
