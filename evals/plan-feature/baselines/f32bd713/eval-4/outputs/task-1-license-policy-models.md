## Repository
trustify-backend

## Target Branch
main

## Description
Create the data models for the license compliance report feature (TC-9004). This includes a JSON-based license policy configuration file that defines which licenses are compliant and which are not, Rust structs to deserialize the policy configuration, and response model structs for the compliance report (license groups with compliance flags). The policy file enables organizations to customize their license compliance rules.

## Files to Create
- `config/license-policy.json` — default license policy configuration defining allowed and denied license lists with SPDX identifiers
- `modules/fundamental/src/sbom/model/license_report.rs` — LicensePolicy, LicenseGroup, and ComplianceReport structs with serde derives

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — export the new license_report module

## Implementation Notes
Follow the existing model struct patterns established in the sbom module. See `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) for the struct definition style with serde derives.

The LicensePolicy struct should deserialize a JSON file containing:
- An allowed-licenses list (SPDX identifiers that are compliant)
- A denied-licenses list (SPDX identifiers that are non-compliant)
- A default-compliance boolean for licenses not in either list

The ComplianceReport struct should serialize to the response format: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`.

Per CONVENTIONS.md §Module pattern: follow the model/ + service/ + endpoints/ structure for the new code. The license report models belong in the model/ directory of the sbom module.
Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's `.rs` module file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference implementation for serde-derived model structs in the sbom module
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — reference implementation for detailed response structs
- `entity/src/package_license.rs` — existing package-license entity mapping; the LicenseGroup model should align with this entity's field names

## Acceptance Criteria
- [ ] LicensePolicy struct successfully deserializes a JSON policy file containing allowed-licenses, denied-licenses, and default-compliance fields
- [ ] ComplianceReport struct serializes to JSON with the expected format: `{ groups: [{ license, packages, compliant }] }`
- [ ] LicenseGroup struct contains license name (String), packages list (Vec), and compliant boolean
- [ ] Default license-policy.json file contains a reasonable set of common open-source licenses categorized as allowed or denied
- [ ] The license_report module is exported from sbom/model/mod.rs

## Test Requirements
- [ ] Unit test: LicensePolicy round-trips through JSON deserialization and re-serialization
- [ ] Unit test: ComplianceReport serializes to the expected JSON structure
- [ ] Unit test: LicensePolicy correctly classifies a license as allowed, denied, or default

## Dependencies
- None
