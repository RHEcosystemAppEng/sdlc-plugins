## Repository
trustify-backend

## Target Branch
main

## Description
Add model types for the license compliance report feature. This includes the response structs for the license report endpoint (`LicenseGroup`, `LicenseReport`) and the license policy configuration types (`LicensePolicy`) that define which licenses are compliant or non-compliant. The policy is loaded from a JSON configuration file stored in the repository, enabling organizations to customize their compliance rules.

This task establishes the foundational types that the service layer (Task 2) and endpoint (Task 3) depend on.

## Files to Create
- `modules/fundamental/src/sbom/license_report/mod.rs` — License report submodule declaration, re-exports model and policy types
- `modules/fundamental/src/sbom/license_report/model.rs` — `LicenseGroup` struct (license name, list of packages, compliant flag) and `LicenseReport` struct (list of LicenseGroups, overall compliance status)
- `modules/fundamental/src/sbom/license_report/policy.rs` — `LicensePolicy` struct with allowed/denied license lists, deserialization from JSON, and a method to evaluate whether a given license identifier is compliant
- `config/license-policy.json` — Default license policy configuration file with example allowed/denied license lists (e.g., MIT, Apache-2.0 allowed; GPL-3.0 flagged)

## Files to Modify
- `modules/fundamental/src/sbom/mod.rs` — Add `pub mod license_report;` to register the new submodule
- `modules/fundamental/Cargo.toml` — Add any required serde dependencies if not already present

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct definitions and serialization derives.
- `LicenseGroup` should implement `Serialize` for JSON API responses. Fields: `license: String`, `packages: Vec<PackageLicenseEntry>`, `compliant: bool`.
- `LicenseReport` should contain `groups: Vec<LicenseGroup>` and optionally a top-level `compliant: bool` field indicating whether all groups are compliant.
- `LicensePolicy` should deserialize from a JSON file using `serde_json`. Include a `fn is_compliant(&self, license: &str) -> bool` method.
- The policy file path should be configurable (e.g., via environment variable or constructor parameter) rather than hardcoded.
- Use SPDX license identifiers as the canonical format for license names.
- Reference the existing `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` which already includes a `license` field — the report model should be compatible with this data.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Contains the `license` field that provides the source data for license grouping. Reuse the same license identifier format.
- `common/src/model/paginated.rs::PaginatedResults` — Reference for response wrapper patterns used in the codebase.
- `common/src/error.rs::AppError` — Use for error types when policy file loading fails.

## Acceptance Criteria
- [ ] `LicenseGroup` struct is defined with license name, package list, and compliant flag fields
- [ ] `LicenseReport` struct is defined with a list of `LicenseGroup` and an overall compliance flag
- [ ] `LicensePolicy` struct deserializes from JSON with allowed/denied license lists
- [ ] `LicensePolicy::is_compliant()` correctly evaluates license identifiers against the policy
- [ ] Default `license-policy.json` config file exists with example configuration
- [ ] All structs derive `Serialize` (and `Deserialize` where needed)

## Test Requirements
- [ ] Unit test: `LicensePolicy` deserializes correctly from valid JSON
- [ ] Unit test: `LicensePolicy::is_compliant()` returns `true` for allowed licenses
- [ ] Unit test: `LicensePolicy::is_compliant()` returns `false` for denied licenses
- [ ] Unit test: `LicensePolicy::is_compliant()` handles unknown licenses according to policy defaults (deny-by-default or allow-by-default)
- [ ] Unit test: `LicenseReport` serializes to expected JSON structure matching the API contract `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Dependencies
- None (foundational task)
