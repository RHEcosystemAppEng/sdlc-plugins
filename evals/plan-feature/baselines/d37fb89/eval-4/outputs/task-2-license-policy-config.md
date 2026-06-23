## Repository
trustify-backend

## Target Branch
main

## Description
Add a configurable license policy mechanism that defines which licenses are compliant and which are not. The policy is stored as a JSON configuration file and loaded at service startup. This policy is used by the license report service to flag non-compliant license groups.

## Files to Create
- `config/license-policy.json` — Default license policy configuration with allowed/denied license lists
- `modules/fundamental/src/sbom/service/license_policy.rs` — `LicensePolicy` struct and `evaluate_compliance()` function that checks a license identifier against the policy

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_policy;` to export the new module

## Implementation Notes
The license policy JSON should follow a simple allow/deny structure:
```json
{
  "allowed_licenses": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC"],
  "denied_licenses": ["GPL-3.0-only", "AGPL-3.0-only"],
  "default_policy": "allow"
}
```

The `LicensePolicy` struct should:
- Deserialize from the JSON config file
- Provide an `is_compliant(license: &str) -> bool` method
- Support a `default_policy` field ("allow" or "deny") for licenses not explicitly listed
- Handle SPDX license identifiers

Follow the error handling pattern from `common/src/error.rs::AppError` for policy loading failures. Use `.context()` wrapping as established in the codebase.

## Reuse Candidates
- `common/src/error.rs::AppError` — reuse for error handling when policy file is missing or malformed

## Acceptance Criteria
- [ ] `config/license-policy.json` contains a sensible default policy with common permissive licenses allowed and common copyleft licenses denied
- [ ] `LicensePolicy` struct deserializes from JSON correctly
- [ ] `is_compliant()` returns `true` for licenses in the allowed list
- [ ] `is_compliant()` returns `false` for licenses in the denied list
- [ ] `is_compliant()` falls back to `default_policy` for unlisted licenses
- [ ] Policy loading errors produce clear `AppError` messages with context

## Test Requirements
- [ ] Unit test: `is_compliant("MIT")` returns `true` with default policy
- [ ] Unit test: `is_compliant("GPL-3.0-only")` returns `false` with default policy
- [ ] Unit test: unlisted license uses `default_policy` correctly for both "allow" and "deny" defaults
- [ ] Unit test: malformed JSON produces a descriptive error

[sdlc-workflow] Description digest: sha256-md:eeef20f8e4c8c5444e81a05047ce3bc5adfd8ae192faf3b4edf627f2ff93e2d8
