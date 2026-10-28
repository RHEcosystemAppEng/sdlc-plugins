## Repository
trustify-backend

## Target Branch
main

## Description
Create the license policy configuration model and the license compliance report response types for feature TC-9004. The license policy defines which licenses are compliant and which are not, loaded from a JSON configuration file. The report model represents the structured API response with packages grouped by license type and compliance flags.

This task establishes the domain types that the service layer (Task 2) and endpoint layer (Task 2) will consume.

## Files to Create
- `common/src/model/license_policy.rs` — LicensePolicy struct with allowed/denied license lists, JSON deserialization, and a method to check whether a given license identifier is compliant
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseGroup struct (license name, packages list, compliant flag) and LicenseReport struct (groups array) with Serialize derives for API response

## Files to Modify
- `common/src/model/mod.rs` — add `pub mod license_policy;` re-export
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod license_report;` re-export

## Implementation Notes
- Follow the existing model struct pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) for derive macros and field annotations.
- Use `serde::Deserialize` for LicensePolicy (loaded from config) and `serde::Serialize` for LicenseReport/LicenseGroup (API response). Both should also derive `Debug` and `Clone`.
- LicensePolicy should support a deny-list approach (licenses explicitly marked as non-compliant) and/or an allow-list approach (only listed licenses are compliant). Use an enum or struct field to indicate the policy mode.
- Policy file loading should use `std::fs::read_to_string` + `serde_json::from_str` with `AppError` wrapping via `.context()` per the project error handling convention.
- The LicenseReport response format must match the Feature specification: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`. Use `#[serde(rename_all = "camelCase")]` if needed to match the expected JSON field casing.
- Reference `entity/src/package_license.rs` for the existing Package-License entity structure to ensure the report model aligns with the data model.
- Per repo Key Conventions: All handlers and service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `common/src/model/license_policy.rs` matching the convention's Rust source scope.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` — reference for response wrapper struct pattern with Serialize derives
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for model struct pattern with serde derives and field annotations
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — includes `license` field, reference for how license data is represented in existing models
- `entity/src/package_license.rs` — existing Package-License mapping entity, defines the data relationship this report aggregates
- `common/src/error.rs::AppError` — error type for `.context()` wrapping on policy file load errors

## Acceptance Criteria
- [ ] LicensePolicy struct can be deserialized from a JSON configuration file with allowed and/or denied license lists
- [ ] LicensePolicy has a method to determine if a given SPDX license identifier is compliant or non-compliant
- [ ] LicenseReport and LicenseGroup structs serialize to the expected JSON format: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- [ ] Policy loading returns an appropriate AppError when the config file is missing or malformed
- [ ] Both modules are correctly re-exported from their parent mod.rs files

## Test Requirements
- [ ] Unit test: deserialize a sample license policy JSON with both allowed and denied license lists
- [ ] Unit test: LicensePolicy correctly classifies a known-compliant license as compliant
- [ ] Unit test: LicensePolicy correctly classifies a known-non-compliant license as non-compliant
- [ ] Unit test: LicenseReport serialization produces the expected JSON output format
- [ ] Unit test: LicensePolicy returns error for malformed JSON input

## Dependencies
- No dependencies
