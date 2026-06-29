# Task 1 — Add license policy configuration model and loader

## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are compliant and which are not. The policy is stored as a JSON config file in the repository. This task creates the data structures and a loader that reads and validates the policy file at startup or on-demand.

## Files to Modify
- `common/src/lib.rs` — add `pub mod license_policy;` module declaration

## Files to Create
- `common/src/license_policy/mod.rs` — `LicensePolicy` struct with `allowed_licenses: Vec<String>`, `denied_licenses: Vec<String>`, and a `is_compliant(license: &str) -> bool` method; includes a `load_from_file(path: &Path) -> Result<LicensePolicy, AppError>` function that reads and deserializes the JSON config
- `license-policy.json` — default license policy configuration file at the repository root with example entries (e.g., MIT and Apache-2.0 as allowed, GPL-3.0 as denied)

## Implementation Notes
- Follow the existing error handling pattern: return `Result<T, AppError>` using `.context()` wrapping, as seen in `common/src/error.rs`
- Use `serde::Deserialize` for the JSON config deserialization, consistent with the existing Cargo workspace dependency patterns
- The policy evaluation logic should be straightforward: a license is compliant if it appears in `allowed_licenses` (when the list is non-empty) or does not appear in `denied_licenses`
- The policy file path should be configurable, not hardcoded — accept it as a parameter to the loader function

## Reuse Candidates
- `common/src/error.rs::AppError` — shared error type with `IntoResponse` implementation; reuse for error propagation from the policy loader

## Acceptance Criteria
- [ ] `LicensePolicy` struct correctly deserializes from a JSON file with `allowed_licenses` and `denied_licenses` arrays
- [ ] `is_compliant` returns `true` for allowed licenses and `false` for denied licenses
- [ ] Loading a malformed or missing policy file returns an appropriate `AppError`
- [ ] A default `license-policy.json` exists at the repo root with documented example entries

## Test Requirements
- [ ] Unit test: `is_compliant` returns `true` for a license in `allowed_licenses`
- [ ] Unit test: `is_compliant` returns `false` for a license in `denied_licenses`
- [ ] Unit test: `is_compliant` handles case where `allowed_licenses` is empty (deny-list mode)
- [ ] Unit test: `load_from_file` returns error for nonexistent file path
- [ ] Unit test: `load_from_file` returns error for invalid JSON content

## Documentation Updates
- `license-policy.json` — document the schema and usage in a comment block or accompanying section in the README
