# Task 1 — Add license policy configuration model

## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy model that defines which licenses are compliant and which are not. The policy is loaded from a JSON configuration file at startup and used by the license report service to flag non-compliant packages. This provides the configurable compliance policy foundation required by the feature.

## Files to Modify
- `common/src/lib.rs` — add `policy` module declaration

## Files to Create
- `common/src/policy/mod.rs` — LicensePolicy struct with allowed/denied license lists, deserialization from JSON, and a `is_compliant(license: &str) -> bool` method
- `common/src/policy/default_policy.json` — default license policy configuration file (example with common permissive licenses as allowed, copyleft licenses as flagged)

## Implementation Notes
- Follow the existing module pattern in `common/src/` — see `common/src/db/mod.rs` and `common/src/model/mod.rs` for established conventions
- Use `serde::Deserialize` for JSON deserialization, consistent with the project's existing serde usage
- The policy struct should support:
  - An `allowed` list of SPDX license identifiers that are considered compliant
  - A `denied` list of SPDX license identifiers that are considered non-compliant
  - A default behavior for licenses not in either list (configurable: default-allow or default-deny)
- Error handling: return `AppError` when the policy file is missing or malformed, following the pattern in `common/src/error.rs`
- The policy file path should be configurable (e.g., via environment variable or server config), but default to an embedded policy

## Reuse Candidates
- `common/src/error.rs::AppError` — use existing error enum for policy loading failures
- `common/src/model/mod.rs` — follow established model organization patterns

## Acceptance Criteria
- [ ] LicensePolicy struct can be deserialized from a JSON file
- [ ] `is_compliant()` correctly returns true for allowed licenses and false for denied licenses
- [ ] Licenses not in either list respect the default behavior setting
- [ ] Policy loading errors produce meaningful error messages via AppError

## Test Requirements
- [ ] Unit test: deserialize a valid policy JSON and verify allowed/denied classification
- [ ] Unit test: verify default behavior for unlisted licenses (both default-allow and default-deny modes)
- [ ] Unit test: verify error handling for malformed JSON input
- [ ] Unit test: verify case-insensitive SPDX identifier matching (e.g., "MIT" matches "mit")

## Dependencies
- None
