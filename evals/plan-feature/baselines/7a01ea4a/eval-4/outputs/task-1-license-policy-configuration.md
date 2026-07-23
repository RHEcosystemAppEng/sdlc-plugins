# Task 1 — Add license policy configuration file and loader

## Repository
trustify-backend

## Target Branch
main

## Description
Add a configurable license policy mechanism that defines which licenses are compliant and which are not. The policy is stored as a JSON configuration file in the repository and loaded at service startup. This provides the foundation for the license compliance report (Task 2) to flag non-compliant packages.

The policy file defines license classifications: an allow-list of approved licenses, a deny-list of prohibited licenses, and a default disposition for licenses not in either list. This supports the MVP requirement that non-compliant licenses are flagged based on a configurable policy.

## Files to Create
- `config/license-policy.json` — Default license policy configuration file with allow/deny lists and default disposition
- `common/src/license_policy.rs` — Policy data types (`LicensePolicy`, `LicenseClassification`) and loader function that reads and deserializes the configuration file

## Files to Modify
- `common/src/lib.rs` — Add `pub mod license_policy;` module declaration
- `common/Cargo.toml` — Add `serde_json` dependency if not already present (for config deserialization)

## Implementation Notes
- Follow the established module pattern: define types with `#[derive(Deserialize, Serialize)]` for the policy configuration structs.
- The policy loader should return `Result<LicensePolicy, AppError>` using the `AppError` enum from `common/src/error.rs` with `.context()` wrapping per the project error handling convention.
  Applies: task creates `common/src/license_policy.rs` matching the convention's Rust module scope.
- The JSON policy file schema should support:
  - `allowed_licenses`: array of SPDX license identifiers that are compliant
  - `denied_licenses`: array of SPDX license identifiers that are non-compliant
  - `default_disposition`: `"compliant"` or `"non-compliant"` for licenses not in either list
- Reference the SPDX license list for standard license identifiers.
- Per project conventions (§Error handling): all error paths must return `Result<T, AppError>` with `.context()` wrapping. See `common/src/error.rs` for the `AppError` enum definition.
  Applies: task creates `common/src/license_policy.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/error.rs::AppError` — Error type for wrapping policy loading failures
- `common/src/lib.rs` — Module registration pattern for adding new submodules

## Acceptance Criteria
- [ ] A default `config/license-policy.json` file exists with a valid schema containing allowed and denied license lists
- [ ] `LicensePolicy` struct can be deserialized from the JSON config file
- [ ] Policy loader returns `AppError` with context on file-not-found or invalid JSON
- [ ] The policy supports SPDX license identifiers

## Test Requirements
- [ ] Unit test: deserialize a valid policy JSON into `LicensePolicy` struct
- [ ] Unit test: verify error handling when policy file is missing
- [ ] Unit test: verify error handling when policy JSON is malformed
- [ ] Unit test: verify license classification lookup (allowed, denied, default disposition)

## Verification Commands
- `cargo build -p common` — compiles without errors
- `cargo test -p common` — all tests pass

## Dependencies
- None (this is a foundational task)
