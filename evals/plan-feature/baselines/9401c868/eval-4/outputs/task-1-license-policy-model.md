## Repository
trustify-backend

## Target Branch
main

## Description
Add the license policy configuration model and compliance report data structures needed by the license compliance report feature (TC-9004). The license policy defines which licenses are allowed or denied for a project. The compliance report models represent the grouped license data returned by the report endpoint.

The policy is stored as a JSON configuration file in the repository and loaded at service initialization. The report models define the response shape: packages grouped by license type, each group annotated with a compliance flag based on the policy.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- License policy struct (`LicensePolicy` with `allowed` and `denied` license lists), compliance report response structs (`LicenseReportGroup` with license name, package list, and `compliant` boolean; `ComplianceReport` wrapping a vector of groups), and a `LicensePolicy::load_from_file()` method that reads and deserializes the JSON config
- `license-policy.json` -- Default license policy configuration file at the repository root with an example structure: `{ "allowed": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause"], "denied": ["GPL-3.0", "AGPL-3.0"] }`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod license_report;` to expose the new module

## Implementation Notes
- Follow the existing model pattern in the SBOM module: `SbomSummary` (in `summary.rs`) and `SbomDetails` (in `details.rs`) demonstrate the struct definition and serialization approach. Use `serde::Deserialize` for the policy config and `serde::Serialize` for the response structs.
- The `ComplianceReport` response shape must match the API contract from the feature requirements: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`. Use `#[serde(rename_all = "camelCase")]` if needed to match JSON field naming conventions used by existing response types.
- The `LicensePolicy::load_from_file()` method should return `Result<Self, AppError>` using the error handling pattern from `common/src/error.rs`.
- Per CONVENTIONS.md: all model structs follow the `model/` directory structure within the domain module.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's `.rs` module scope.
- Per CONVENTIONS.md: error handling uses `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- Demonstrates the struct definition, serde derives, and field naming conventions for SBOM model types
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- Contains the `license` field that the compliance report will reference when grouping packages
- `common/src/error.rs::AppError` -- Error enum used for the policy loader's error return type

## Acceptance Criteria
- [ ] `LicensePolicy` struct deserializes from a JSON file with `allowed` and `denied` license lists
- [ ] `LicensePolicy::load_from_file()` returns `Result<LicensePolicy, AppError>` and produces a clear error when the file is missing or malformed
- [ ] `LicenseReportGroup` struct contains `license` (String), `packages` (Vec), and `compliant` (bool) fields
- [ ] `ComplianceReport` struct contains a `groups` field (Vec<LicenseReportGroup>)
- [ ] Response structs serialize to the JSON shape specified in the feature requirements
- [ ] `license-policy.json` contains a valid default policy with common permissive and copyleft licenses
- [ ] Module is exported via `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test: `LicensePolicy` deserializes from valid JSON with both `allowed` and `denied` fields
- [ ] Unit test: `LicensePolicy::load_from_file()` returns an error for missing file
- [ ] Unit test: `LicensePolicy::load_from_file()` returns an error for malformed JSON
- [ ] Unit test: `ComplianceReport` serializes to the expected JSON shape matching `{ groups: [{ license, packages, compliant }] }`

## Dependencies
- None (this is the first task in the chain)
