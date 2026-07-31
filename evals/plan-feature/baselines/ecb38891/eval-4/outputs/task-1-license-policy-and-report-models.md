## Repository
trustify-backend

## Target Branch
main

## Description
Add the data models for the license compliance report feature. This includes:
1. A license policy configuration model that loads compliance rules from a JSON config file, defining which licenses are approved, restricted, or banned.
2. License report response models (LicenseGroup, LicenseReport) that represent the grouped license data with compliance flags returned by the API.

The policy configuration file is stored in the repository and loaded at service startup. Organizations can customize the policy by modifying the JSON file to match their compliance requirements.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReport and LicenseGroup structs representing the API response: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- `modules/fundamental/src/sbom/model/license_policy.rs` — LicensePolicy struct with deserialization from JSON, containing approved/restricted/banned license lists
- `license-policy.json` — Default license policy configuration file with example approved licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) and example restricted licenses (GPL-3.0, AGPL-3.0)

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod license_report;` and `pub mod license_policy;` module declarations

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — derive `Serialize`, `Deserialize`, `Clone`, `Debug` on all structs.
- Per Key Conventions §Module pattern: follow the `model/ + service/ + endpoints/` structure. Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` and `modules/fundamental/src/sbom/model/license_policy.rs` matching the convention's model directory scope.
- Per Key Conventions §Error handling: use `Result<T, AppError>` with `.context()` wrapping for policy file loading errors. Applies: task creates `modules/fundamental/src/sbom/model/license_policy.rs` which loads configuration and must handle I/O errors.
- The LicenseGroup struct should include: `license` (String — the SPDX license identifier), `packages` (Vec of package references), and `compliant` (bool — whether this license passes the policy).
- The LicensePolicy struct should support loading from a file path, with a `is_compliant(&self, license: &str) -> bool` method.

## Reuse Candidates
- `entity/src/package_license.rs::PackageLicense` — existing Package-License mapping entity; use this as the source of license data rather than creating a new entity
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — includes a `license` field; reference this struct's pattern for license-related model design

## Acceptance Criteria
- [ ] LicenseReport struct can be serialized to JSON matching the response format: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- [ ] LicensePolicy struct can deserialize from a JSON configuration file
- [ ] LicensePolicy correctly classifies licenses as compliant or non-compliant based on its rules
- [ ] Default `license-policy.json` file exists with a reasonable set of approved and restricted licenses
- [ ] Module declarations are added to `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test: LicensePolicy deserialization from valid JSON config
- [ ] Unit test: LicensePolicy `is_compliant` returns true for approved licenses
- [ ] Unit test: LicensePolicy `is_compliant` returns false for restricted/banned licenses
- [ ] Unit test: LicenseReport serialization produces expected JSON structure
- [ ] Unit test: LicensePolicy handles unknown licenses (not in any list) according to policy default

## Dependencies
- None (first task in the feature)
