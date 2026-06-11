# Task 1 — Add license policy configuration model and loader

## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are allowed, denied, or flagged for review. The policy is stored as a JSON configuration file in the repository and loaded at service initialization. This provides the foundation for the compliance checking logic in subsequent tasks.

## Files to Create
- `common/src/license_policy.rs` — LicensePolicy struct and JSON deserialization logic; a loader function that reads the policy from a configurable file path
- `license-policy.json` — Default license policy configuration file at the repository root with common allowed licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) and denied licenses (GPL-3.0, AGPL-3.0)

## Files to Modify
- `common/src/lib.rs` — Add `pub mod license_policy;` to expose the new module
- `common/Cargo.toml` — Add `serde_json` dependency if not already present for JSON deserialization

## Implementation Notes
- Follow the existing module pattern in `common/src/` where shared types and utilities live.
- The `LicensePolicy` struct should contain:
  - `allowed: Vec<String>` — licenses that are always compliant
  - `denied: Vec<String>` — licenses that are never compliant
  - `review_required: Vec<String>` — licenses that need manual review (flagged but not auto-denied)
- Use `serde::Deserialize` for the struct, consistent with how other configuration types are handled in the codebase.
- The loader function should accept a file path parameter and return `Result<LicensePolicy, AppError>`, following the error handling pattern in `common/src/error.rs` with `.context()` wrapping.
- Use SPDX license identifiers as the standard format for license strings in the policy configuration.
- Per `docs/constraints.md` section 5: changes must be scoped to the listed files only. Follow patterns found in existing code rather than introducing new patterns.

## Reuse Candidates
- `common/src/error.rs::AppError` — Use the existing error type for configuration loading failures

## Acceptance Criteria
- [ ] `LicensePolicy` struct is defined with `allowed`, `denied`, and `review_required` fields
- [ ] JSON deserialization works correctly for a well-formed policy file
- [ ] Loader function returns a clear error when the policy file is missing or malformed
- [ ] Default `license-policy.json` file is present with reasonable defaults

## Test Requirements
- [ ] Unit test: deserialize a valid license policy JSON string into `LicensePolicy`
- [ ] Unit test: deserialization fails gracefully with a malformed JSON input
- [ ] Unit test: loader returns appropriate error for missing file path

## Verification Commands
- `cargo build -p common` — compiles without errors
- `cargo test -p common` — all tests pass

## Dependencies
- None
