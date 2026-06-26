## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration mechanism that defines which licenses are approved and which are denied. The policy is stored as a JSON configuration file and loaded at startup. This enables the license report to flag packages with non-compliant licenses.

## Files to Create
- `common/src/license_policy.rs` — Define `LicensePolicy` struct and loader function that reads the policy from a JSON config file
- `license-policy.json` — Default license policy configuration file at the project root with example approved/denied license lists

## Files to Modify
- `common/src/lib.rs` — Add `pub mod license_policy;` to expose the new module

## Implementation Notes
- The `LicensePolicy` struct should contain: `allowed_licenses: Vec<String>` (SPDX identifiers that are approved), `denied_licenses: Vec<String>` (SPDX identifiers that are explicitly denied), and `default_policy: PolicyDefault` enum (`Allow` or `Deny`) controlling how unlisted licenses are treated.
- Provide a `LicensePolicy::load(path: &Path) -> Result<Self, AppError>` method that reads and deserializes the JSON config file using `serde_json`.
- Provide a `LicensePolicy::is_compliant(&self, license: &str) -> bool` method that checks a license identifier against the policy: denied licenses return false, allowed licenses return true, unlisted licenses follow `default_policy`.
- Use `common/src/error.rs::AppError` for error handling with `.context()` wrapping.
- The default `license-policy.json` should include common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as allowed and known copyleft licenses (GPL-3.0-only, AGPL-3.0-only) as denied, with `default_policy: "deny"` for a secure default.

## Reuse Candidates
- `common/src/error.rs::AppError` — Standard error type for the project; use for policy loading errors

## Acceptance Criteria
- [ ] `LicensePolicy` struct loads from a JSON file and exposes `is_compliant` method
- [ ] Default policy file exists with sensible defaults for common SPDX license identifiers
- [ ] Unknown licenses are handled according to `default_policy` setting
- [ ] Loading a malformed or missing config file returns a descriptive `AppError`

## Test Requirements
- [ ] Unit test: allowed license returns `is_compliant = true`
- [ ] Unit test: denied license returns `is_compliant = false`
- [ ] Unit test: unlisted license follows `default_policy` (test both Allow and Deny defaults)
- [ ] Unit test: loading invalid JSON returns an error

[sdlc-workflow] Description digest: sha256-md:ccdc5f430f099f81e604de018ea6f6e07801b202a36389c7fa8710cf21f6c73f
