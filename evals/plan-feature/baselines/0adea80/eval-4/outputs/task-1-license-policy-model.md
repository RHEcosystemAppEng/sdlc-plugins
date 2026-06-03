# Task 1 — Add license policy configuration model and loader

## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are compliant and which are non-compliant for the project. The policy is stored as a JSON configuration file in the repository and loaded at service startup. This forms the foundation for the compliance evaluation in the license report endpoint.

## Files to Create
- `common/src/model/license_policy.rs` — LicensePolicy struct with allowed/denied license lists, JSON deserialization, and policy evaluation method
- `config/default-license-policy.json` — Default license policy configuration file with common open-source license classifications

## Files to Modify
- `common/src/model/mod.rs` — Add `pub mod license_policy;` to expose the new module
- `common/Cargo.toml` — Add serde_json dependency if not already present

## Implementation Notes
- Follow the existing model pattern in `common/src/model/` — see `paginated.rs` for the struct + derive pattern used in this crate.
- The `LicensePolicy` struct should include:
  - `allowed_licenses: Vec<String>` — SPDX identifiers for licenses that are compliant
  - `denied_licenses: Vec<String>` — SPDX identifiers for licenses that are non-compliant
  - `default_policy: PolicyDefault` — enum (`Allow` or `Deny`) controlling how licenses not in either list are treated
- Implement a `is_compliant(&self, license: &str) -> bool` method that checks a license identifier against the policy.
- Use `serde::Deserialize` for JSON deserialization, consistent with how other models in `common/` derive serde traits.
- Per the NFR, the policy is a JSON config file in the repo — not a database table.

## Reuse Candidates
- `common/src/model/paginated.rs` — Demonstrates the struct + derive macro pattern used in the common crate
- `common/src/error.rs` — `AppError` enum for consistent error handling when policy loading fails

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from a JSON file
- [ ] `is_compliant()` correctly classifies allowed, denied, and unlisted licenses based on default policy
- [ ] A default license policy JSON file exists with reasonable defaults (e.g., MIT, Apache-2.0 as allowed; GPL-3.0 as denied)

## Test Requirements
- [ ] Unit test: deserialize a valid policy JSON string into `LicensePolicy`
- [ ] Unit test: `is_compliant` returns true for allowed licenses
- [ ] Unit test: `is_compliant` returns false for denied licenses
- [ ] Unit test: `is_compliant` respects the `default_policy` for unlisted licenses
- [ ] Unit test: handle malformed policy JSON gracefully (return error, not panic)

## Verification Commands
- `cargo test -p common` — all tests pass including new license policy tests
