# Task 1 — Add license policy configuration model

## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are compliant and which are non-compliant. The policy is stored as a JSON configuration file in the repository and loaded at startup. This provides the foundation for the compliance checking logic in subsequent tasks.

## Files to Create
- `common/src/model/license_policy.rs` — LicensePolicy struct with deserialization from JSON, containing allowed and denied license lists
- `license-policy.json` — Default license policy configuration file at the repository root with example SPDX license identifiers

## Files to Modify
- `common/src/model/mod.rs` — Add `pub mod license_policy;` to export the new module
- `common/src/lib.rs` — Re-export the license policy model if needed for cross-module access
- `common/Cargo.toml` — Add `serde_json` dependency if not already present (for config file parsing)

## Implementation Notes
- Follow the existing model pattern established in `common/src/model/paginated.rs` — define a struct with `#[derive(Debug, Clone, Serialize, Deserialize)]`
- The LicensePolicy struct should contain:
  - `allowed_licenses: Vec<String>` — SPDX identifiers for explicitly allowed licenses (e.g., "MIT", "Apache-2.0")
  - `denied_licenses: Vec<String>` — SPDX identifiers for explicitly denied licenses (e.g., "GPL-3.0-only")
  - `default_policy: PolicyDefault` — enum indicating whether unlisted licenses are allowed or denied by default
- Include a `LicensePolicy::load(path: &Path) -> Result<Self, AppError>` method for loading from the JSON file
- Use `common/src/error.rs` `AppError` for error handling, consistent with existing error patterns
- The JSON config file format should be straightforward and documented with comments in a README section

## Reuse Candidates
- `common/src/error.rs::AppError` — Use the existing error enum for configuration loading errors
- `common/src/model/paginated.rs` — Follow its derive macro and struct patterns as a model reference

## Acceptance Criteria
- [ ] LicensePolicy struct can be deserialized from a JSON configuration file
- [ ] Default license-policy.json exists with example allowed/denied license lists
- [ ] Loading a malformed JSON file returns an appropriate AppError
- [ ] LicensePolicy is accessible from other modules in the workspace

## Test Requirements
- [ ] Unit test: deserialize a valid license policy JSON string into LicensePolicy
- [ ] Unit test: verify deserialization fails with appropriate error for malformed JSON
- [ ] Unit test: verify a license is correctly matched against allowed/denied lists
- [ ] Unit test: verify default_policy behavior for licenses not in either list

## Dependencies
- None
