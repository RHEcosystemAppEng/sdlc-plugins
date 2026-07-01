# Task 1 -- Add license policy configuration model

**Summary:** Add license policy configuration model and loader

**Priority:** Major
**Fix Versions:** RHTPA 1.5.0
**Labels:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are compliant and which are not. The policy is stored as a JSON config file in the repository and loaded at startup. This provides the foundation for the license compliance report feature by establishing the rules against which package licenses are evaluated.

## Files to Create
- `common/src/license_policy/mod.rs` -- license policy module with `LicensePolicy` struct, JSON deserialization, and policy lookup methods
- `license-policy.json` -- default license policy configuration file at the repository root

## Files to Modify
- `common/src/lib.rs` -- add `pub mod license_policy` to expose the new module
- `common/Cargo.toml` -- add serde_json dependency if not already present

## Implementation Notes
- Follow the existing module pattern in `common/src/` -- see `common/src/db/mod.rs` and `common/src/model/mod.rs` for the established structure
- The `LicensePolicy` struct should contain:
  - `allowed_licenses: Vec<String>` -- SPDX license identifiers that are compliant (allowlist)
  - `denied_licenses: Vec<String>` -- SPDX license identifiers that are explicitly non-compliant (denylist)
  - A method `is_compliant(&self, license: &str) -> bool` that checks a license identifier against the policy. If `denied_licenses` is non-empty and the license is in it, return false. If `allowed_licenses` is non-empty and the license is not in it, return false. Otherwise return true.
- Use `serde::Deserialize` for JSON deserialization, following the same pattern as other config types in the codebase
- The default `license-policy.json` should contain a reasonable set of common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC) as allowed and known copyleft licenses (GPL-2.0, GPL-3.0, AGPL-3.0) as denied
- Per CONVENTIONS.md (Key Conventions -- Error handling): use `Result<T, AppError>` with `.context()` wrapping for policy loading errors. Applies: task creates `common/src/license_policy/mod.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `common/src/error.rs::AppError` -- existing error enum for consistent error handling
- `common/src/model/mod.rs` -- reference for module structure patterns

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from a JSON configuration file
- [ ] `is_compliant()` correctly evaluates licenses against allow/deny lists
- [ ] Default `license-policy.json` is present with sensible defaults
- [ ] Policy loading errors produce descriptive `AppError` messages with context

## Test Requirements
- [ ] Unit test: `LicensePolicy::is_compliant` returns true for allowed licenses
- [ ] Unit test: `LicensePolicy::is_compliant` returns false for denied licenses
- [ ] Unit test: `LicensePolicy::is_compliant` returns false for unlisted licenses when allowlist is non-empty
- [ ] Unit test: deserialization from valid JSON succeeds
- [ ] Unit test: deserialization from malformed JSON returns an error

## Dependencies
- None

[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000001
