# Task 2 — Add license compliance report model

## Repository
trustify-backend

## Target Branch
main

## Description
Add the response model for the license compliance report. The report groups packages by license type and flags each group as compliant or non-compliant based on the license policy. This model is the response type for the license report endpoint.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReportResponse, LicenseGroup, and PackageLicenseInfo structs

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new module

## Implementation Notes
- Follow the model struct pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — use `#[derive(Clone, Debug, Serialize, Deserialize)]` with serde.
- The response structure must match the feature specification:
  ```
  LicenseReportResponse {
    groups: Vec<LicenseGroup>
  }
  
  LicenseGroup {
    license: String,          // SPDX license identifier
    packages: Vec<PackageLicenseInfo>,  // packages with this license
    compliant: bool           // whether this license is compliant per policy
  }
  
  PackageLicenseInfo {
    name: String,             // package name
    version: String,          // package version
    transitive: bool          // whether this is a transitive dependency
  }
  ```
- The `PackageSummary` struct in `modules/fundamental/src/sbom/model/../../../package/model/summary.rs` includes a `license` field — reference this for the license data shape coming from the database.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs` — `SbomSummary` struct pattern for serde derives and field naming
- `modules/fundamental/src/sbom/model/details.rs` — `SbomDetails` struct pattern for nested response types
- `modules/fundamental/src/package/model/summary.rs` — `PackageSummary` with the `license` field that maps to package license data

## Acceptance Criteria
- [ ] `LicenseReportResponse` struct exists with a `groups` field of type `Vec<LicenseGroup>`
- [ ] `LicenseGroup` struct includes `license`, `packages`, and `compliant` fields
- [ ] `PackageLicenseInfo` struct includes `name`, `version`, and `transitive` fields
- [ ] All structs derive `Serialize` for JSON API responses

## Test Requirements
- [ ] Unit test: serialize `LicenseReportResponse` to JSON and verify the output matches the expected shape `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`

## Dependencies
- Depends on: Task 1 — Add license policy configuration model and loader (uses `LicensePolicy` for compliance evaluation context)
