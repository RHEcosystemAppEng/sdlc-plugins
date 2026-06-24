## Repository
trustify-backend

## Target Branch
main

## Description
Implement a configurable license policy mechanism that determines which licenses are compliant. The policy is stored as a JSON configuration file at the project root and loaded by the service layer. This enables organizations to define their own allow/deny lists for open-source licenses.

## Files to Create
- `license-policy.json` — Default license policy configuration file with an allow-list of common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) and a deny-list of restrictive licenses (GPL-3.0, AGPL-3.0)
- `modules/fundamental/src/sbom/service/license_policy.rs` — Policy loading and evaluation logic: parse the JSON config, expose a `LicensePolicy` struct with an `is_compliant(license: &str) -> bool` method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_policy;` to expose the policy module

## Implementation Notes
- The policy JSON structure should be: `{ "allowed": ["MIT", "Apache-2.0", ...], "denied": ["GPL-3.0", ...], "default_policy": "allow" | "deny" }` where `default_policy` governs licenses not in either list
- Load the policy file path from an environment variable (e.g., `TRUSTIFY_LICENSE_POLICY_PATH`) with a fallback to `./license-policy.json`
- Follow the service module pattern from `modules/fundamental/src/sbom/service/sbom.rs` for struct organization
- Use `serde_json` for deserialization, consistent with the project's existing JSON handling
- The `LicensePolicy` struct should be cloneable and cacheable so it is loaded once at startup

## Acceptance Criteria
- [ ] `license-policy.json` exists at the project root with a sensible default policy
- [ ] `LicensePolicy` struct loads and parses the configuration file
- [ ] `is_compliant()` correctly evaluates licenses against allow/deny lists and the default policy
- [ ] Missing or malformed policy files produce clear error messages via `AppError` from `common/src/error.rs`

## Test Requirements
- [ ] Unit tests verify `is_compliant()` returns true for allowed licenses
- [ ] Unit tests verify `is_compliant()` returns false for denied licenses
- [ ] Unit tests verify default policy behavior for unlisted licenses
- [ ] Unit tests verify graceful error handling for missing or invalid config files

## Digest
[sdlc-workflow] Description digest: sha256-md:7b92892ba4f748650468498f81dd1507b1ef08da07d2dd34118b495ae4a848c2
