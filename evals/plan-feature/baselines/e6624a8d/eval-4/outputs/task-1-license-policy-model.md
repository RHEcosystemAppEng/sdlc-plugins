## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are compliant and which are non-compliant for the project. The policy is stored as a JSON config file in the repository and loaded at runtime. This model is consumed by the license report service (Task 2) to flag non-compliant packages.

## Files to Create
- `common/src/model/license_policy.rs` — License policy model: `LicensePolicy` struct with fields for allowed licenses, denied licenses, and default compliance behavior; includes deserialization from JSON and a `is_compliant(license: &str) -> bool` method
- `license-policy.json` — Default license policy configuration file at the repository root with common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as allowed and copyleft licenses (GPL-2.0, GPL-3.0, AGPL-3.0) as flagged

## Files to Modify
- `common/src/model/mod.rs` — Add `pub mod license_policy;` to expose the new module
- `common/Cargo.toml` — Add `serde_json` dependency if not already present for JSON deserialization

## Implementation Notes
- Follow the existing model pattern in `common/src/model/` — see `paginated.rs` for the established struct + derive macro pattern
- Use `serde::Deserialize` for JSON deserialization of the policy file
- The policy model should support both an explicit allowlist and denylist approach, with a `default_compliance` field (bool) that determines the compliance status of licenses not in either list
- Reference the SPDX license identifier format for license string matching
- Per docs/constraints.md section 5 (Code Change Rules): changes must be scoped to listed files; inspect code before modifying; follow patterns in Implementation Notes
- Per CONVENTIONS.md -- Module pattern: follow the model/ + service/ + endpoints/ structure when placing new model types. Applies: task creates `common/src/model/license_policy.rs` matching the convention's `.rs` model file scope.
- Per CONVENTIONS.md -- Error handling: use `Result<T, AppError>` with `.context()` wrapping for fallible operations. Applies: task creates `common/src/model/license_policy.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` — demonstrates the established pattern for model structs with serde derives in the common crate
- `common/src/error.rs::AppError` — use for policy file loading errors with `.context()` wrapping

## Acceptance Criteria
- [ ] `LicensePolicy` struct deserializes from a JSON configuration file
- [ ] `is_compliant(license: &str) -> bool` method correctly evaluates licenses against allowlist and denylist
- [ ] Default `license-policy.json` file exists at repository root with sensible defaults
- [ ] Licenses not in either list respect the `default_compliance` fallback

## Test Requirements
- [ ] Unit test: `LicensePolicy` deserializes from valid JSON
- [ ] Unit test: `is_compliant` returns true for allowed licenses
- [ ] Unit test: `is_compliant` returns false for denied licenses
- [ ] Unit test: `is_compliant` respects `default_compliance` for unlisted licenses
- [ ] Unit test: deserialization fails gracefully with invalid JSON

## Dependencies
- None (this is the first task)
