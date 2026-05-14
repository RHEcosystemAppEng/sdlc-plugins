# Task 1 — Add license compliance policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Add a configurable license compliance policy that defines which licenses are allowed, denied, or flagged for review. The policy is stored as a JSON configuration file in the repository and loaded at startup. This policy is the foundation for the license compliance report endpoint (Task 3), which uses it to determine whether each package's license is compliant.

## Files to Create
- `config/license-policy.json` — Default license compliance policy defining allowed and denied license SPDX identifiers
- `common/src/license_policy.rs` — LicensePolicy struct and deserialization logic; policy loading from config file path

## Files to Modify
- `common/src/lib.rs` — Add `pub mod license_policy;` to expose the new module
- `common/Cargo.toml` — Add serde_json dependency if not already present
- `server/src/main.rs` — Load the license policy at startup and make it available as Axum shared state

## Implementation Notes
- Follow the existing module pattern in `common/src/` — see `common/src/error.rs` for the established pattern of standalone modules in the common crate.
- The policy JSON should use SPDX license identifiers (e.g., "MIT", "Apache-2.0", "GPL-3.0-only") and define categories: `allowed` (list of compliant licenses), `denied` (list of non-compliant licenses), and `review_required` (licenses requiring manual review).
- Use `serde::Deserialize` to parse the policy file, consistent with the SeaORM entity patterns.
- Load the policy file path from an environment variable (e.g., `LICENSE_POLICY_PATH`) with a default fallback to `config/license-policy.json`.
- Make the loaded `LicensePolicy` available via Axum's `Extension` or state extractor so downstream handlers can access it.
- Per docs/constraints.md section 2 (Commit Rules): commits must reference TC-9004, follow Conventional Commits, and include the `Assisted-by: Claude Code` trailer.
- Per docs/constraints.md section 5 (Code Change Rules): inspect existing code before modifying, follow patterns in Implementation Notes, do not duplicate existing functionality.

## Reuse Candidates
- `common/src/error.rs` — Follow this module's structure for adding a new standalone module in the common crate
- `server/src/main.rs` — Reference existing state/extension setup patterns for Axum shared state

## Acceptance Criteria
- [ ] A default `config/license-policy.json` file exists with a reasonable set of allowed and denied licenses
- [ ] `LicensePolicy` struct correctly deserializes from the JSON file
- [ ] Policy is loaded at server startup and available as shared state
- [ ] Missing or malformed policy file produces a clear error at startup, not a panic

## Test Requirements
- [ ] Unit test: `LicensePolicy` deserializes a valid policy JSON correctly
- [ ] Unit test: `LicensePolicy` returns a meaningful error for malformed JSON
- [ ] Unit test: `LicensePolicy::is_compliant(license_id)` returns correct results for allowed, denied, and review_required licenses
- [ ] Unit test: unknown licenses (not in any category) are handled with a defined default behavior

## Dependencies
- None
