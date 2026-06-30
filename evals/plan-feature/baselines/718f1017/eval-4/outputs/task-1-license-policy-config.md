# Task 1 -- Add license policy configuration model and loader

## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are compliant and which are not. The policy is stored as a JSON config file in the repository and loaded at service startup. This provides the foundation for the license compliance report feature (TC-9004), enabling organizations to define their own compliance rules.

## Files to Create
- `common/src/model/license_policy.rs` -- LicensePolicy struct and JSON deserialization logic; loader function that reads the policy from a config file path
- `license-policy.json` -- Default license policy configuration file at the repository root with common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) marked as compliant and a deny-list placeholder

## Files to Modify
- `common/src/model/mod.rs` -- Add `pub mod license_policy;` to expose the new module
- `common/Cargo.toml` -- Add serde_json dependency if not already present (for JSON config deserialization)

## Implementation Notes
- Follow the existing model pattern in `common/src/model/` -- see `paginated.rs` for the struct + derive pattern used in this module.
- The LicensePolicy struct should derive `Deserialize` and `Clone` at minimum, following the serde patterns already used in the codebase (e.g., `common/src/model/paginated.rs`).
- The policy JSON schema should support:
  - `allowed_licenses`: array of SPDX license identifiers that are considered compliant
  - `denied_licenses`: array of SPDX license identifiers that are explicitly non-compliant
  - `default_policy`: either `"allow"` or `"deny"` for licenses not in either list
- Use `serde_json::from_reader` to load the policy file, returning `Result<LicensePolicy, AppError>` consistent with the error handling pattern in `common/src/error.rs`.
- Per CONVENTIONS.md (repository conventions): the module follows the established `model/` directory pattern for shared data structures.
  Applies: task creates `common/src/model/license_policy.rs` matching the convention's Rust module scope.

## Reuse Candidates
- `common/src/error.rs::AppError` -- Use the existing AppError enum for error handling in the policy loader, following the `.context()` wrapping pattern.
- `common/src/model/paginated.rs` -- Reference for struct derive patterns and module organization within `common/src/model/`.

## Acceptance Criteria
- [ ] A `LicensePolicy` struct exists that can be deserialized from a JSON configuration file
- [ ] A default `license-policy.json` file exists at the repository root with sensible defaults
- [ ] The policy loader function reads the file and returns a typed `LicensePolicy` or an `AppError`
- [ ] The policy supports allowed/denied license lists and a default policy setting

## Test Requirements
- [ ] Unit test: deserialize a valid license policy JSON string into a `LicensePolicy` struct
- [ ] Unit test: deserialize a policy with only `allowed_licenses` set (minimal config)
- [ ] Unit test: loading a non-existent policy file returns an appropriate `AppError`
- [ ] Unit test: deserialize a policy with unknown fields fails gracefully or ignores them (depending on serde config)

## Dependencies
- None

<!-- [sdlc-workflow] Description digest: sha256-md:5117b62e72a669ff90df51b22c0967a30a94b55a2b1807f155f9d6ca91cabaf7 -->
