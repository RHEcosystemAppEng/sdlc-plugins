## Repository
trustify-backend

## Target Branch
main

## Description
Define the license policy configuration schema and model types. This task introduces a JSON-based license policy configuration file that specifies which licenses are approved, restricted, or denied. It also adds the Rust model types for deserializing and validating the policy.

## Files to Modify
- `common/src/model/mod.rs` — Add re-export for the new license_policy module

## Files to Create
- `common/src/model/license_policy.rs` — LicensePolicy, LicenseClassification (Approved/Restricted/Denied) structs with serde Deserialize. Includes a `classify(&self, license_id: &str) -> LicenseClassification` method and a `load_from_file(path: &Path) -> Result<Self>` loader.
- `etc/license-policy.json` — Default license policy configuration file. Contains `approved_licenses` (e.g., MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause), `restricted_licenses` (e.g., LGPL-2.1, MPL-2.0), and `denied_licenses` (e.g., GPL-3.0, AGPL-3.0) lists, plus a `default_policy` field set to `"restricted"` for unlisted licenses.

## Implementation Notes
- Follow the existing model pattern in `common/src/model/` where types derive `Serialize, Deserialize, Clone, Debug`.
- Use `serde_json` for deserialization, consistent with the project's existing dependencies.
- The policy file path should be configurable via an environment variable (e.g., `TRUST_LICENSE_POLICY_PATH`) with a sensible default of `etc/license-policy.json`.
- The `LicenseClassification` enum should have three variants: `Approved`, `Restricted`, `Denied`.

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from a JSON file
- [ ] `classify()` method correctly categorizes known and unknown licenses
- [ ] Default policy file is present and valid JSON
- [ ] Policy loading returns a clear error if the file is missing or malformed

## Test Requirements
- [ ] Unit test: deserialize a sample policy JSON and verify classification of approved, restricted, denied, and unlisted licenses
- [ ] Unit test: verify error handling for invalid JSON input

## Dependencies
- None — this is the foundational task
