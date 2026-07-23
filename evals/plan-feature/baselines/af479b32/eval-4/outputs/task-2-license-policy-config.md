# Task 2 — Add license policy configuration

**Summary:** Add license policy configuration and loader

**Epic:** TC-9004: License report data layer

## Repository
trustify-backend

## Target Branch
main

## Description
Add a configurable license compliance policy that defines which licenses are allowed or denied. The policy is stored as a JSON configuration file in the repository and loaded at startup. The license report service (Task 3) will use this policy to determine the `compliant` flag for each license group.

## Files to Create
- `modules/fundamental/src/sbom/service/license_policy.rs` — defines `LicensePolicy` struct (with `allowed` and `denied` license lists) and a `load_policy` function that reads and parses the JSON config file
- `license-policy.json` — default license policy configuration file at the repository root, with example entries for common permissive and copyleft licenses

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod license_policy` to register the new module

## Implementation Notes
- The `LicensePolicy` struct should contain:
  - `allowed_licenses: Vec<String>` — list of SPDX identifiers considered compliant (e.g., "MIT", "Apache-2.0", "BSD-3-Clause")
  - `denied_licenses: Vec<String>` — list of SPDX identifiers considered non-compliant (e.g., "GPL-3.0-only", "AGPL-3.0-only")
  - A compliance check method: `fn is_compliant(&self, license: &str) -> bool` — returns `true` if the license is in the allowed list and not in the denied list; if a license appears in neither list, it should default to non-compliant (deny-by-default)
- Use `serde_json` for JSON parsing, consistent with the existing crate dependencies
- Follow the error handling pattern from `common/src/error.rs` — return `Result<T, AppError>` from the loader function with `.context()` wrapping for file I/O errors
- The default `license-policy.json` should include a representative set of common licenses to serve as a starting point that organizations can customize
- Follow the service module pattern from `modules/fundamental/src/sbom/service/mod.rs` for module organization

## Reuse Candidates
- `common/src/error.rs::AppError` — the standard error type; use for error handling in the policy loader
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — demonstrates the existing service module structure and error handling patterns

## Acceptance Criteria
- [ ] `LicensePolicy` struct is defined with `allowed_licenses` and `denied_licenses` fields
- [ ] `is_compliant()` method correctly identifies compliant and non-compliant licenses
- [ ] Policy can be loaded from a JSON file using `load_policy()`
- [ ] A default `license-policy.json` file exists at the repository root with example entries
- [ ] Invalid or missing policy file produces a clear error via `AppError`

## Test Requirements
- [ ] Test that `is_compliant()` returns `true` for allowed licenses
- [ ] Test that `is_compliant()` returns `false` for denied licenses
- [ ] Test that `is_compliant()` returns `false` for unknown licenses (deny-by-default)
- [ ] Test that `load_policy()` correctly parses a valid JSON policy file
- [ ] Test that `load_policy()` returns an error for invalid JSON

## Dependencies
- None
