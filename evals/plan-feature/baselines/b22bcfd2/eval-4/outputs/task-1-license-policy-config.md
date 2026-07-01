## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model and default policy file. The policy defines which licenses are approved, restricted, or denied for compliance evaluation. This is the foundation that the license report service will use to flag non-compliant packages.

## Files to Create
- `modules/fundamental/src/sbom/model/license_policy.rs` — Structs for `LicensePolicy`, `LicensePolicyEntry` with serde deserialization; enum `LicenseCompliance { Approved, Restricted, Denied }`
- `config/default-license-policy.json` — Default license policy JSON file listing common licenses (MIT, Apache-2.0, BSD-2-Clause as approved; GPL-3.0, AGPL-3.0 as restricted; unlicensed as denied)

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_policy;` to expose the new module

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/`. Use `serde::Deserialize` and `serde::Serialize` derives matching the style in `summary.rs` and `details.rs`. The policy struct should support loading from a JSON file at startup and provide a lookup method `fn check_license(&self, license_id: &str) -> LicenseCompliance`.

Per CONVENTIONS.md: conventions are not referenced here as no CONVENTIONS.md content was provided in the fixture beyond noting its existence.

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from the default JSON config file
- [ ] Default policy file contains at least 5 common SPDX license identifiers with compliance classifications
- [ ] `check_license()` returns the correct compliance status for known and unknown licenses
- [ ] Unknown licenses default to `Restricted` classification

## Test Requirements
- [ ] Unit test: deserialize default-license-policy.json into LicensePolicy struct
- [ ] Unit test: check_license returns Approved for MIT, Restricted for GPL-3.0, Denied for unlicensed
- [ ] Unit test: check_license returns Restricted for unrecognized license identifiers

## Dependencies
None
