# Task 2 — Add license compliance report model

## Repository
trustify-backend

## Target Branch
main

## Description
Define the response model structs for the license compliance report. These structs represent the grouped license data returned by the report endpoint, with compliance flags indicating whether each license group conforms to the configured policy.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReport and LicenseGroup structs

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new model module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/` — see `summary.rs` and `details.rs` for struct conventions (derive macros, field naming, serialization attributes).
- Define the following structs:
  - `LicenseGroup` — represents a single license grouping:
    - `license: String` — the SPDX license identifier
    - `packages: Vec<PackageLicenseEntry>` — list of packages with this license
    - `compliant: bool` — whether this license is compliant per the configured policy
    - `policy_status: String` — one of "allowed", "denied", or "review_required"
  - `PackageLicenseEntry` — a lightweight package reference within a license group:
    - `name: String` — package name
    - `version: String` — package version
    - `transitive: bool` — whether this is a transitive (indirect) dependency
  - `LicenseReport` — the top-level response:
    - `sbom_id: String` — the SBOM identifier
    - `groups: Vec<LicenseGroup>` — license groups
    - `total_packages: usize` — total number of packages analyzed
    - `compliant_count: usize` — number of compliant license groups
    - `non_compliant_count: usize` — number of non-compliant license groups
- All structs must derive `Serialize` (and `Deserialize` for testing) using serde, consistent with existing model structs.
- Per `docs/constraints.md` section 4.7: reference existing patterns. Follow the serialization and naming patterns in `SbomSummary` and `SbomDetails`.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Follow the same derive macro pattern and field naming conventions
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — Reference for nested struct composition
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Has `license` field; reference for package-license data shape

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseGroup`, and `PackageLicenseEntry` structs are defined with all specified fields
- [ ] All structs derive `Serialize` for JSON response serialization
- [ ] The module is publicly accessible from the sbom model module

## Test Requirements
- [ ] Unit test: serialize a `LicenseReport` with multiple groups to JSON and verify the output structure matches the expected shape `{ sbom_id, groups: [{ license, packages: [...], compliant, policy_status }], ... }`
- [ ] Unit test: verify an empty report serializes correctly with zero counts

## Dependencies
- None
