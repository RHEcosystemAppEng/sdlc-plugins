## Repository

trustify-backend

## Target Branch

main

## Description

Add a default license policy configuration file and the loading logic to read it at startup. The policy defines which licenses are compliant and which are flagged as non-compliant, supporting the configurable compliance checking required by the license report feature.

## Files to Modify

- `common/src/lib.rs` — add the license policy module to the common crate exports
- `server/src/main.rs` — load the license policy config at server startup and register it as shared application state (Axum extension)

## Files to Create

- `config/license-policy.json` — default license policy configuration file listing common compliant licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) and flagging copyleft licenses (GPL-2.0, GPL-3.0, AGPL-3.0) as non-compliant by default
- `common/src/service/license_policy.rs` — `LicensePolicyService` that loads the policy from disk, validates it, and provides a `check_compliance(license: &str) -> bool` method

## Implementation Notes

- The license policy JSON file follows the structure defined by the `LicensePolicy` model from Task 1
- Policy loading should use `std::fs::read_to_string` with a configurable path, defaulting to `config/license-policy.json`
- Follow the error handling pattern from `common/src/error.rs` — wrap I/O errors with `.context()` producing `AppError`
- Register the loaded `LicensePolicyService` as an Axum `Extension` in `server/src/main.rs`, following the same pattern used for other shared services
- Licenses not explicitly listed in the policy should default to compliant (allow-by-default with a deny-list approach)
- License identifiers should be compared case-insensitively using SPDX normalization

## Acceptance Criteria

- A valid `config/license-policy.json` exists with sensible defaults for common open-source licenses
- `LicensePolicyService` loads the policy file and provides compliance checking
- The service is registered as shared application state at server startup
- `cargo check` passes with no errors

## Test Requirements

- Unit test for `LicensePolicyService::check_compliance` verifying that MIT returns compliant and GPL-3.0 returns non-compliant given the default policy
- Unit test verifying graceful error handling when the policy file is missing (returns an appropriate error, does not panic)
- Unit test verifying case-insensitive license matching (e.g., "mit" matches "MIT")
