# Task 2 — Add license report response model

## Repository
trustify-backend

## Target Branch
main

## Description
Create the response model structs for the license compliance report. The report groups packages by license type and includes a compliance flag per group based on the license policy. This model is consumed by the report endpoint and produced by the report service.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Structs: `LicenseReport` (contains `groups: Vec<LicenseGroup>`), `LicenseGroup` (contains `license: String`, `packages: Vec<LicensePackageRef>`, `compliant: bool`), `LicensePackageRef` (contains package identifier, name, version, and whether it is a transitive dependency).

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new module.

## Implementation Notes
- Follow the existing model conventions in `modules/fundamental/src/sbom/model/` — see `summary.rs` and `details.rs` for derive macro usage (`Serialize`, `Debug`, `Clone`) and field naming conventions.
- The response must match the shape specified in the feature: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`.
- Use `serde::Serialize` (and optionally `Deserialize` for testing) on all structs.
- `LicensePackageRef` should include enough information for the consumer to identify the package (e.g., purl or name + version) plus a `transitive: bool` field indicating whether it is a direct or transitive dependency.
- Per docs/constraints.md §5.2: inspect existing code before implementing. Review `SbomSummary` and `SbomDetails` in `modules/fundamental/src/sbom/model/` for the conventions on response struct design.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — example of response model struct with serde derives.
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — example of detailed response model with nested collections.
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — package model showing the fields available for `LicensePackageRef`.

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseGroup`, and `LicensePackageRef` structs are defined with appropriate serde derives
- [ ] Serialization produces the expected JSON shape: `{ "groups": [{ "license": "...", "packages": [...], "compliant": true/false }] }`
- [ ] `LicensePackageRef` includes package identifier, name, version, and transitive flag

## Test Requirements
- [ ] Unit test: serialize a `LicenseReport` with multiple groups and verify the JSON output matches the expected shape
- [ ] Unit test: verify that an empty report (no groups) serializes correctly

## Dependencies
- Depends on: Task 1 — Add license policy configuration model and loader (uses `LicensePolicy` disposition to set `compliant` flag)
