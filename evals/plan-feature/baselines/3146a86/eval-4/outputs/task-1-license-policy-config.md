# Task 1 — Add license policy configuration model and loader

## Repository
trustify-backend

## Target Branch
main

## Description
Define the license compliance policy data model and a loader that reads the policy from a JSON configuration file. The policy specifies which licenses are allowed, denied, or flagged for review. This is the foundation for the license compliance report — without a policy, the report cannot determine whether a license is compliant.

## Files to Create
- `modules/fundamental/src/sbom/model/license_policy.rs` — Structs for `LicensePolicy`, `LicenseRule` (license SPDX identifier + disposition: allow/deny/review). Includes a `load_from_file(path)` function and a `check_license(spdx_id) -> Disposition` method.
- `config/license-policy.json` — Default license policy configuration file with a reasonable baseline (e.g., MIT/Apache-2.0 allowed, GPL-3.0 flagged for review).

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_policy;` to expose the new module.

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/` — see `summary.rs` and `details.rs` for struct definition conventions (derive macros, serde attributes).
- Use `serde::Deserialize` for the policy struct so it can be loaded from JSON.
- The policy file path should be configurable (e.g., via an environment variable or server config), but default to `config/license-policy.json` at the repo root.
- Use SPDX license identifiers as the canonical key for license matching (e.g., `MIT`, `Apache-2.0`, `GPL-3.0-only`).
- The `check_license` method should support case-insensitive matching against SPDX identifiers.
- Per docs/constraints.md §5.2: inspect existing code before implementing. Review the `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` to understand how the `license` field is stored, ensuring the policy matches against the same format.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the `license` field format that the policy must match against.
- `common/src/error.rs::AppError` — use for error handling when the policy file is missing or malformed.

## Acceptance Criteria
- [ ] `LicensePolicy` struct deserializes from a JSON file containing allowed/denied license rules
- [ ] `check_license(spdx_id)` returns the correct disposition (allow/deny/review) for known licenses
- [ ] `check_license(spdx_id)` returns a default disposition (e.g., review) for licenses not listed in the policy
- [ ] Loading a nonexistent or malformed policy file returns a descriptive `AppError`

## Test Requirements
- [ ] Unit test: deserialize a valid policy JSON and verify license rules are loaded correctly
- [ ] Unit test: `check_license` returns allow for allowed licenses, deny for denied licenses, review for unlisted licenses
- [ ] Unit test: loading from a nonexistent path returns an appropriate error
- [ ] Unit test: loading from a malformed JSON file returns a parse error
