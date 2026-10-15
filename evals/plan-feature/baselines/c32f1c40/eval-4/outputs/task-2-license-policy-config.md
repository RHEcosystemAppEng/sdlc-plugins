## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration module that reads a JSON-based license compliance policy file and evaluates whether a given SPDX license identifier is compliant. The policy defines allowed and denied license patterns, enabling organizations to configure their own compliance rules.

## Files to Create
- `common/src/license_policy.rs` — `LicensePolicy` struct and `LicensePolicyConfig` loader that reads and parses the JSON policy file, plus an `is_compliant(license: &str) -> bool` method

## Files to Modify
- `common/src/lib.rs` — Add `pub mod license_policy;` to expose the new module
- `common/Cargo.toml` — Add `serde_json` dependency if not already present

## Implementation Notes
- The policy file format should be a JSON file with a structure like:
  ```json
  {
    "allowed_licenses": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause"],
    "denied_licenses": ["GPL-3.0-only", "AGPL-3.0-only"],
    "default_policy": "allow"
  }
  ```
- When `default_policy` is `"allow"`, only licenses in `denied_licenses` are non-compliant. When `"deny"`, only licenses in `allowed_licenses` are compliant.
- Use the existing error handling pattern from `common/src/error.rs` — return `Result<T, AppError>` with `.context()` wrapping for file I/O errors.
  Applies: task creates `common/src/license_policy.rs` matching the convention's Rust source file scope.
- Per Key Conventions (Error handling): all functions return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `common/src/license_policy.rs` matching the convention's Rust source file scope.
- The policy file path should be configurable (e.g., via environment variable or constructor parameter), not hardcoded.
- Use SPDX license identifiers as the canonical license format for matching.

## Reuse Candidates
- `common/src/error.rs::AppError` — reuse for error handling in policy loading
- `common/src/db/mod.rs` — reference for module organization pattern in the common crate

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from a JSON file
- [ ] `is_compliant(license: &str) -> bool` correctly evaluates licenses against the policy
- [ ] `allowed_licenses` and `denied_licenses` lists are respected based on `default_policy`
- [ ] Missing or unreadable policy file returns a clear `AppError` with context
- [ ] Module is re-exported from `common/src/lib.rs`

## Test Requirements
- [ ] Unit test: policy with `default_policy: "allow"` marks denied licenses as non-compliant
- [ ] Unit test: policy with `default_policy: "deny"` marks only allowed licenses as compliant
- [ ] Unit test: loading from a valid JSON file succeeds
- [ ] Unit test: loading from a missing file returns an appropriate error
- [ ] Unit test: empty allowed/denied lists behave correctly with both default policies

## Dependencies
- None
