## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model and loader that reads a JSON config file defining the organization's license compliance policy. The policy specifies which licenses are allowed, denied, or flagged for review. This model is consumed by the license report service (Task 2) to determine compliance status for each package license.

## Files to Create
- `common/src/model/license_policy.rs` — Define `LicensePolicy` struct with fields for allowed licenses, denied licenses, and review-required licenses; implement a loader that reads the policy from a JSON config file path
- `license-policy.json` — Default license policy configuration file at the repository root with example entries for common open-source licenses (MIT, Apache-2.0, GPL-3.0, etc.)

## Files to Modify
- `common/src/model/mod.rs` — Add `pub mod license_policy;` to re-export the new module
- `common/Cargo.toml` — Add `serde` and `serde_json` dependencies if not already present

## Implementation Notes
- The `LicensePolicy` struct should derive `Deserialize` and `Clone` so it can be loaded from JSON and shared across request handlers
- Include a `LicensePolicy::load(path: &Path) -> Result<Self, AppError>` method that reads and parses the JSON config file, wrapping errors with `.context("Failed to load license policy")` for consistent error handling
- The policy JSON schema should support three categories: `allowed` (list of SPDX identifiers that are compliant), `denied` (list of SPDX identifiers that are non-compliant), and `review_required` (list of identifiers needing manual review). Packages with licenses not in any list default to `review_required`
- Per CONVENTIONS.md Key Conventions (Error Handling): all fallible operations must return `Result<T, AppError>` with `.context()` wrapping for meaningful error messages.
  Applies: task creates `common/src/model/license_policy.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md Key Conventions (Framework): use `serde` for JSON deserialization, consistent with the SeaORM entity pattern used throughout the project.
  Applies: task creates `common/src/model/license_policy.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `common/src/error.rs::AppError` — the standard error type; use this for all error returns from the policy loader
- `common/src/model/mod.rs` — existing model module pattern to follow for re-export structure

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from a JSON config file
- [ ] The loader returns a clear `AppError` when the config file is missing or malformed
- [ ] Default `license-policy.json` contains at least: MIT, Apache-2.0 as allowed; GPL-3.0 as review_required
- [ ] Policy supports allowed, denied, and review_required license categories

## Test Requirements
- [ ] Unit test: load a valid policy JSON and verify all three categories are parsed correctly
- [ ] Unit test: load a malformed JSON file and verify an appropriate error is returned
- [ ] Unit test: load from a nonexistent path and verify a file-not-found error is returned

## Verification Commands
- `cargo test --package common` — all unit tests pass
- `cargo build --package common` — compiles without errors

## Dependencies
- None (this is the first task)
