## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are compliant and which are not. The policy is loaded from a JSON configuration file in the repository, enabling organizations to customize their compliance rules. This supports the core requirement of flagging non-compliant licenses based on a configurable policy.

## Files to Create
- `common/src/model/license_policy.rs` -- LicensePolicy struct with JSON loading logic and compliance evaluation methods

## Files to Modify
- `common/src/model/mod.rs` -- add `pub mod license_policy;` to expose the new module

## Implementation Notes
- The `LicensePolicy` struct should contain:
  - `allowed_licenses: Vec<String>` -- SPDX identifiers that are explicitly compliant
  - `denied_licenses: Vec<String>` -- SPDX identifiers that are explicitly non-compliant
  - `default_policy: PolicyDefault` -- enum (Allow or Deny) for licenses not in either list
- Implement `LicensePolicy::from_file(path: &Path) -> Result<Self, AppError>` to load policy from a JSON configuration file.
- Implement `LicensePolicy::is_compliant(&self, license: &str) -> bool` to evaluate a single SPDX license identifier against the policy:
  1. If the license is in `denied_licenses`, return false.
  2. If the license is in `allowed_licenses`, return true.
  3. Otherwise, return based on `default_policy` (Allow -> true, Deny -> false).
- The `LicensePolicy` struct must derive `serde::Deserialize` for JSON loading and `serde::Serialize` for potential API exposure.
- Use `common/src/error.rs::AppError` for error handling, wrapping file I/O and JSON parse errors with `.context()`.
- Follow the struct organization pattern in `common/src/model/paginated.rs` for placement within the common module.

- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` from the policy loading function and use `.context()` wrapping for error propagation.
  Applies: task creates `common/src/model/license_policy.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` -- reference for struct patterns and derive macros in the common module
- `common/src/error.rs::AppError` -- error type to use for policy loading and parsing failures

## Acceptance Criteria
- [ ] `LicensePolicy` struct is defined with `allowed_licenses`, `denied_licenses`, and `default_policy` fields
- [ ] `PolicyDefault` enum is defined with `Allow` and `Deny` variants
- [ ] `from_file` loads and parses a JSON policy configuration file
- [ ] `is_compliant` correctly evaluates a license string: denied -> false, allowed -> true, unlisted -> default policy
- [ ] Errors during file loading or JSON parsing are wrapped with `AppError` and contextual messages
- [ ] Module is re-exported from `common/src/model/mod.rs`
- [ ] Project compiles without errors

## Test Requirements
- [ ] Unit test: `is_compliant` returns `true` for a license in the allowed list
- [ ] Unit test: `is_compliant` returns `false` for a license in the denied list
- [ ] Unit test: `is_compliant` respects the default policy for unlisted licenses (both Allow and Deny defaults)
- [ ] Unit test: `from_file` returns an error with context for a malformed JSON file
- [ ] Unit test: `from_file` returns an error with context for a non-existent file path

## Verification Commands
- `cargo check -p trustify-common` -- expected: compiles without errors
- `cargo test -p trustify-common` -- expected: all unit tests pass

## Dependencies
- None

---

[sdlc-workflow] Description digest: sha256-md:d2a87d0e91b5588f2f8ec76882e82d3326e2ab849aa621e93ad928474093c7b9
