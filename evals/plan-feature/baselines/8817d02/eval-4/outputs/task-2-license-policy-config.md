# Task 2 — Add configurable license policy support

## Repository
trustify-backend

## Target Branch
main

## Description
Implement a configurable license policy mechanism that defines which licenses are compliant and which are not. The policy is stored as a JSON configuration file in the repository and loaded at service startup. This policy is used by the license report service (Task 3) to flag non-compliant license groups.

## Files to Create
- `modules/fundamental/src/sbom/service/license_policy.rs` — define `LicensePolicy` struct and loading logic
- `license-policy.json` — default license policy configuration file at the repository root

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — re-export `license_policy` module

## Implementation Notes
- The `LicensePolicy` struct should contain:
  - `allowed_licenses: Vec<String>` — list of SPDX license identifiers considered compliant (e.g., "MIT", "Apache-2.0", "BSD-2-Clause")
  - `denied_licenses: Vec<String>` — list of SPDX license identifiers explicitly denied
  - A method `is_compliant(&self, license: &str) -> bool` that returns `true` if the license is in the allowed list or not in the denied list (depending on policy mode)
- Follow the existing service module pattern in `modules/fundamental/src/sbom/service/mod.rs` — the policy module sits alongside the sbom service.
- The default `license-policy.json` should contain a reasonable default with common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC) as allowed and common copyleft licenses (GPL-2.0, GPL-3.0, AGPL-3.0) as denied.
- Use `serde_json` for deserialization, consistent with the project's existing JSON handling.
- Load the policy file path from an environment variable or config parameter, with a fallback to `license-policy.json` at the project root.
- Per docs/constraints.md section 5 (Code Change Rules): follow existing patterns; do not duplicate existing config loading logic.
- Error handling: return `Result<LicensePolicy, AppError>` using the `AppError` enum from `common/src/error.rs` with `.context()` wrapping, consistent with the project's error handling pattern.

## Reuse Candidates
- `common/src/error.rs::AppError` — use the existing error type for policy loading failures
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — follow the service struct pattern for dependency injection and initialization

## Acceptance Criteria
- [ ] `LicensePolicy` struct with `allowed_licenses` and `denied_licenses` fields is defined
- [ ] `is_compliant()` method correctly classifies licenses based on the policy
- [ ] Default `license-policy.json` file exists with reasonable defaults
- [ ] Policy loads successfully from a JSON file
- [ ] Missing or malformed policy file produces a clear error via `AppError`

## Test Requirements
- [ ] Unit test: `is_compliant` returns `true` for an allowed license
- [ ] Unit test: `is_compliant` returns `false` for a denied license
- [ ] Unit test: `is_compliant` handles a license not in either list (default behavior)
- [ ] Unit test: policy deserialization from a valid JSON string succeeds
- [ ] Unit test: policy deserialization from an invalid JSON string produces an error

## Dependencies
- None

sha256-md:43c42be0671d33b3c883bd8f2bc1fa29dfe72f9afe0d69c6891281c9130bd6f2
