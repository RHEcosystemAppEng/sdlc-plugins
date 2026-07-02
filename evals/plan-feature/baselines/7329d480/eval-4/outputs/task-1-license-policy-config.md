## Repository
trustify-backend

## Target Branch
main

## Description
Create the license policy configuration model and a default policy JSON file. The license policy defines which licenses are approved, restricted, or prohibited for use in SBOM dependencies. This model will be consumed by the license compliance service to evaluate packages against organizational policy.

## Files to Create
- `config/license-policy.json` — Default license policy file with categorized SPDX license identifiers (approved, restricted, prohibited)
- `common/src/model/license_policy.rs` — Rust structs for deserializing and representing the license policy configuration

## Files to Modify
- `common/src/model/mod.rs` — Add `pub mod license_policy;` re-export
- `common/Cargo.toml` — Add `serde_json` dependency if not already present (for loading JSON config)

## Implementation Notes
- Follow the existing model pattern in `common/src/model/` where `paginated.rs` defines shared response types. The `license_policy.rs` module should define `LicensePolicy`, `LicenseCategory` (approved/restricted/prohibited), and a loader function that reads the JSON config from a configurable path.
- The default `config/license-policy.json` should include common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as approved, weak copyleft licenses (LGPL-2.1, MPL-2.0) as restricted, and strong copyleft licenses (GPL-2.0, GPL-3.0, AGPL-3.0) as prohibited. Use SPDX license identifiers.
- Use `serde::Deserialize` for the policy structs to enable JSON deserialization.
- Per CONVENTIONS.md §Error handling: return `Result<LicensePolicy, AppError>` from the loader function with `.context()` wrapping on file I/O errors. Applies: task creates `common/src/model/license_policy.rs` matching the convention's .rs scope.
- Per CONVENTIONS.md §Module pattern: place the policy model in the `common/src/model/` directory following the established model/service/endpoints structure. Applies: task creates `common/src/model/license_policy.rs` matching the convention's module organization scope.

## Reuse Candidates
- `common/src/error.rs::AppError` — Error type for wrapping policy loading failures

## Acceptance Criteria
- [ ] `config/license-policy.json` exists with a valid default policy containing approved, restricted, and prohibited license categories
- [ ] `LicensePolicy` struct can be deserialized from the JSON config file
- [ ] Policy loading returns `Result<LicensePolicy, AppError>` with descriptive error messages for missing or malformed config
- [ ] `common/src/model/mod.rs` re-exports the `license_policy` module

## Test Requirements
- [ ] Unit test: deserialize a valid license policy JSON string into `LicensePolicy`
- [ ] Unit test: loading a non-existent config file returns an appropriate `AppError`
- [ ] Unit test: a malformed JSON file returns a deserialization error

## Dependencies
- None (this is a foundational task)

## additional_fields
```json
{ "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```
