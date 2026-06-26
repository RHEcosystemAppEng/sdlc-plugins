## Repository
trustify-backend

## Target Branch
main

## Description
Define the response model types for the license compliance report endpoint and the license policy configuration types. The license report groups packages by license type and flags non-compliant licenses based on a configurable policy. This task creates the data structures that the service and endpoint layers will use.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Response model structs: `LicenseReport`, `LicenseGroup` (containing license name, package list, and compliance flag)
- `modules/fundamental/src/sbom/model/license_policy.rs` — Policy configuration types: `LicensePolicy` with allowed/denied license lists, loaded from a JSON config file

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Register the new `license_report` and `license_policy` submodules and re-export their public types

## Implementation Notes
Follow the existing model pattern in the SBOM module. `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` and `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs` demonstrate the conventions for struct definitions, serde derives, and module registration.

The `LicenseReport` struct should contain:
- A vector of `LicenseGroup` entries
- Each `LicenseGroup` has: `license: String`, `packages: Vec<PackageRef>`, `compliant: bool`
- `PackageRef` is a lightweight struct with package name and version (avoid pulling in the full `PackageSummary`)

The `LicensePolicy` struct should:
- Deserialize from JSON using serde
- Support an `allowed_licenses` list (allowlist mode) or `denied_licenses` list (denylist mode)
- Include a method to check whether a given license string is compliant

The response JSON shape is: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`

Per CONVENTIONS.md §Module Pattern: follow the `model/ + service/ + endpoints/` structure for new domain types.
Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's module structure scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference for struct definition patterns, serde derives, and field naming conventions
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — Reference for how detail-level models are structured
- `entity/src/package_license.rs` — The existing entity that maps packages to licenses; the model types should align with this entity's fields

## Acceptance Criteria
- [ ] `LicenseReport` struct serializes to the specified JSON shape with `groups` array
- [ ] `LicenseGroup` contains `license`, `packages`, and `compliant` fields
- [ ] `LicensePolicy` deserializes from JSON and supports both allowlist and denylist modes
- [ ] `LicensePolicy::is_compliant(license: &str) -> bool` method correctly evaluates compliance
- [ ] New types are re-exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test: `LicensePolicy` with allowed_licenses correctly marks known licenses as compliant and unknown as non-compliant
- [ ] Unit test: `LicensePolicy` with denied_licenses correctly marks denied licenses as non-compliant
- [ ] Unit test: `LicenseReport` serializes to the expected JSON structure

[sdlc-workflow] Description digest: sha256-md:5a29efffca49e13484712c75865d454f5d8e1d6292ce8d4fccec809c5f2c066d
